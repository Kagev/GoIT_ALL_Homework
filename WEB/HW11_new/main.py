# import time
# from connect import get_db
# from datetime import date, timedelta
# from models import ContactCreate, Contact, ContactListResponse, ContactBase
from fastapi import FastAPI, Depends, HTTPException, Query, status, Request
# from sqlalchemy.orm import Session
# from sqlalchemy import text
# from models import ContactBase

app = FastAPI()


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}

#
# class ContactResponse(ContactBase):
#     id: int
#     first_name: str
#     last_name: str
#     email: str
#     phone_number: str
#     birth_date: date
#     additional_info: str
#
#
# def sqlalchemy_to_pydantic(contact):
#     return ContactBase(**contact.__dict__)
#
#
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["My-Process-Time"] = str(process_time)
#     response.headers.update({"server": "GoIt web 8 group"})
#     # response.headers["server"] = "Django"
#     return response
#
#
# @app.get("/", name='Корінь проекту')
# def read_root():
#     return {"message": "REST APP v1.0"}
#
#
# @app.get("/api/healthchecker")
# def healthchecker(db: Session = Depends(get_db)):
#     try:
#         # Make request
#         result = db.execute(text("SELECT 1")).fetchone()
#         print(result)
#         if result is None:
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                                 detail="Database is not configured correctly")
#         return {"message": "Welcome to FastAPI!"}
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Error connecting to the database")
#

#
#
# @app.get("/contacts/", response_model=ContactListResponse)
# def get_contacts(db: Session = Depends(get_db), query: str = Query(None, title="Search Query")):
#     if query:
#         contacts = db.query(Contact).filter(
#             Contact.first_name.ilike(f"%{query}%") |
#             Contact.last_name.ilike(f"%{query}%") |
#             Contact.email.ilike(f"%{query}%")
#         ).all()
#     else:
#         contacts = db.query(Contact).all()
#     db.close()
#     return {"contacts": contacts}
#
#
# @app.post("/contacts/create", response_model=ContactCreate)
# def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
#     db_contact = Contact(**contact.dict())
#     db.add(db_contact)
#     db.commit()
#     db.refresh(db_contact)
#     return {"message": "Contact created successfully"}
#
#
# @app.get("/contacts/{contact_id}", response_model=ContactListResponse)
# def get_contact(contact_id: int, db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter(Contact.id == contact_id).first()
#     db.close()
#     if contact is None:
#         raise HTTPException(status_code=404, detail="Contact not found")
#     return {"contacts": [sqlalchemy_to_pydantic(contact)]}
#
#
# @app.put("/contacts/{contact_id}", response_model=ContactResponse)
# def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
#     db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
#     if db_contact is None:
#         db.close()
#         raise HTTPException(status_code=404, detail="Contact not found")
#     for key, value in contact.dict().items():
#         setattr(db_contact, key, value)
#     db.commit()
#     db.refresh(db_contact)
#     db.close()
#     return db_contact
#
#
# @app.delete("/contacts/{contact_id}", response_model=ContactResponse)
# def delete_contact(contact_id: int, db: Session = Depends(get_db)):
#     db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
#     if db_contact is None:
#         db.close()
#         raise HTTPException(status_code=404, detail="Contact not found")
#     db.delete(db_contact)
#     db.commit()
#     db.close()
#     return db_contact
#
#
# @app.get("/contacts/upcoming_birthdays/", response_model=ContactListResponse)
# def get_upcoming_birthdays(db: Session = Depends(get_db), days: int = 7):
#     today = date.today()
#     future_date = today + timedelta(days=days)
#     contacts = db.query(Contact).filter(
#         Contact.birth_date >= today,
#         Contact.birth_date <= future_date
#     ).all()
#     db.close()
#     return contacts
