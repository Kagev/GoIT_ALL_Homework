import pickle
import redis
from redis_lru import RedisLRU
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from config import setting

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from connect import get_db
from models import User

app = FastAPI()
token_auth_scheme = HTTPBearer()
redis_client = redis.StrictRedis(setting.REDIS_HOST, setting.REDIS_PORT, setting.REDIS_PASSWORD)
cache = RedisLRU(redis_client)


class Hash:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


async def generate_token(data: dict, expires_delta: timedelta = None, is_access_token=True):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        if is_access_token:
            expire = datetime.utcnow() + timedelta(minutes=15)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "scope": "access_token" if is_access_token else "refresh_token"})
    token = jwt.encode(to_encode, setting.JWT_SECRET_KEY, algorithm=setting.ALGORITHM)
    return token


async def create_access_token(data: dict, expires_delta: timedelta = None):
    encoded_access_token = await generate_token(data, expires_delta)
    return encoded_access_token


async def create_refresh_token(data: dict, expires_delta: timedelta = None):
    encoded_refresh_token = await generate_token(data, expires_delta, is_access_token=False)
    return encoded_refresh_token


async def get_email_from_refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, setting.JWT_SECRET_KEY, algorithm=setting.ALGORITHM)
        if payload["scope"] == "refresh_token":
            email = payload["sub"]
            return email
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not find valid scope")
    except JWTError as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not find valid credentials")


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
                           db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT
        payload = jwt.decode(token.credentials, setting.JWT_SECRET_KEY, algorithm=setting.ALGORITHM)
        email = payload["sub"]
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user: User | None = db.query(User).filter(User.email == email).first()
    user = redis_client.get(f"user:{email}")
    if user is None:
        user = await db.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        redis_client.set(f"user:{email}", pickle.dumps(user))
        redis_client.expire(f"user:{email}", 900)
    else:
        user = pickle.loads(user)
    if user is None:
        raise credentials_exception
    return user


def generate_verification_link(email: str, minutes: int) -> str:
    expiration_datetime = datetime.utcnow() + timedelta(minutes=minutes)
    data = {"email": email, "exp": expiration_datetime}
    token = jwt.encode(data, setting.JWT_SECRET_KEY.encode('utg-8'), algorithm=setting.ALGORITHM)
    return f"/verify-email?token={token}"


def generate_password_reset_link(email: str, minutes: int) -> str:
    expiration_datetime = datetime.utcnow() + timedelta(minutes=minutes)
    data = {"email": email, "exp": expiration_datetime}
    token = jwt.encode(data, setting.JWT_SECRET_KEY, algorithm=setting.ALGORITHM)
    return f"/reset-password?token={token}"
