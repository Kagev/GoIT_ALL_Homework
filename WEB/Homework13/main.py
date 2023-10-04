import time
import redis
import pickle
from redis_lru import RedisLRU

import connect
from connect import get_db
from datetime import date, timedelta
from fastapi import BackgroundTasks,FastAPI, Depends, HTTPException, Query, status, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Contact, User, EmailSchema, PasswordResetRequest, PasswordResetSettings
from models import ContactBase, ContactListResponse, ContactCreate, ContactResponse, ContactChange, UserModel
from auth import Hash, get_current_user, create_access_token, create_refresh_token, get_email_from_refresh_token, \
    generate_verification_link, generate_password_reset_link
from config import setting
from jose import jwt, JWTError




app = FastAPI()
fast_mail = FastMail(connect.conf)
redis_client = redis.StrictRedis(setting.REDIS_HOST, setting.REDIS_PORT, setting.REDIS_PASSWORD)
cache = RedisLRU(redis_client)
hash_handler = Hash()
password_reset_settings = PasswordResetSettings()

security = HTTPBearer

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5432",
    "http://localhost:6379",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def sqlalchemy_to_pydantic(contact):
    return ContactBase(**contact.__dict__)


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    response.headers.update({"server": "GoIt web 8 group"})
    response.headers["server"] = "Django"
    return response


@app.post("/signup")
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user: User | None = db.query(User).filter_by(email=body.email).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    new_user = User(username=body.username, email=body.email, password=hash_handler.get_password_hash(body.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"new_user": new_user.email}


@app.post("/login")
async def login(body: UserModel, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=body.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await create_access_token(data={"sub": user.email})
    refresh_token = await create_refresh_token(data={"sub": user.email})
    return {"access token": access_token, "refresh token": refresh_token, "token_type": "bearer"}


@app.get("/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security),
                        db: Session = Depends(get_current_user)):
    token = credentials.credentials
    email = await get_email_from_refresh_token(token)
    user = db.query(User).filter_by(email=email).first()
    if user.refresh_token != token:
        user.refresh_token = None
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")
    access_token = await create_access_token(data={"sub": user.email})
    refresh_token = await create_refresh_token(data={"sub": user.email})
    return {"access token": access_token, "refresh token": refresh_token, "token_type": "bearer"}


@app.get("/contacts/", response_model=ContactListResponse)
async def get_contacts(current_user: User = Depends(get_current_user), query: str = Query(None, title="Search Query")):
    if query:
        contacts = current_user.query(Contact).filter(
            Contact.first_name.ilike(f"%{query}%") |
            Contact.last_name.ilike(f"%{query}%") |
            Contact.email.ilike(f"%{query}%")
        ).all()
    else:
        contacts = current_user.query(Contact).all()
    current_user.close()
    return {"contacts": contacts}


@app.post("/contacts/create", response_model=ContactResponse)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.get("/contacts/{contact_id}", response_model=ContactListResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.close()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"contacts": [sqlalchemy_to_pydantic(contact)]}


@app.put("/contacts/{contact_id}", response_model=ContactChange)
async def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        db.close()
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    db.close()
    return db_contact


@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    db_contact = current_user.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        db.close()
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    db.close()
    return db_contact


@app.get("/contacts/upcoming_birthdays/", response_model=ContactListResponse)
async def get_upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(get_current_user),
                                 days: int = 7):
    try:
        today = date.today()
        future_date = today + timedelta(days=days)
        contacts = db.query(Contact).filter(
            Contact.birth_date >= today,
            Contact.birth_date <= future_date
        ).all()
        db.close()
        return {"contacts": contacts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    message = MessageSchema(
        subject="HW13 - Fastapi mail module",
        recipients=[body.email],
        body={"fullname": "GOIT"},
        subtype="html",
    )

    try:
        await fast_mail.send_message(message)
        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"message": f"Email sending failed: {str(e)}"}


@app.post("/send-verification-email")
async def send_verification_email(email: str, email_verification_settings=None):
    # Створіть та надішліть лист із посиланням для верифікації
    verification_link = generate_verification_link(email, email_verification_settings.VERIFY_EMAIL_EXPIRE_MINUTES)
    # Надішліть лист із посиланням для верифікації на вказану адресу


# Маршрут для обробки запитів на верифікацію
@app.get("/verify-email")
async def verify_email(token: str):
    try:
        payload = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=[setting.ALGORITHM])
        email = payload["email"]
        # Позначте користувача як верифікованого в базі даних
        # Або відповідним чином обробіть верифікацію
        return {"message": "Email verified successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid")


@app.post("/send-password-reset-email")
async def send_password_reset_email(request: PasswordResetRequest):
    email = request.email

    password_reset_link = generate_password_reset_link(email, password_reset_settings.PASSWORD_RESET_EXPIRE_MINUTES)

    message_body = f"Для скидання паролю перейдіть за посиланням: {password_reset_link}"

    message = MessageSchema(
        subject="Відновлення паролю",
        recipients=[email],  # Вказати email отримувача
        body=message_body,
    )

    await fast_mail.send_message(message)
    return {"message": "Лист із посиланням для скидання паролю надіслано на ваш email."}


@app.post("/reset-password")
async def reset_password(token: str, new_password: str):
    try:
        payload = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=[setting.ALGORITHM])
        email = payload["email"]
        # Змініть пароль користувача в базі даних на новий пароль
        return {"message": "Password reset successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid")
