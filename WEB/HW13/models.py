import datetime

from pydantic_settings import BaseSettings

from connect import engine
from datetime import date
from pydantic import BaseModel, field_validator, BaseConfig, EmailStr
from sqlalchemy import Column, Integer, String, Date, func, Boolean
from sqlalchemy.orm import declarative_base
from typing import List, Optional

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    birth_date = Column(Date)
    additional_info = Column(String, nullable=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', Date, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_info: Optional[str] = None


class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_info: Optional[str] = None

    @field_validator("email", check_fields=False)
    def email_address_validator(cls, val):
        if not "@" in val:
            raise ValueError("Invalid email")
        return val


class EmailSchema(BaseModel):
    email: EmailStr


class ContactListResponse(BaseModel):
    contacts: List[ContactBase]

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class ContactResponse(ContactBase):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_info: str


class ContactChange(ContactBase):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_info: str


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime.datetime
    avatar: str

    class Config:
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class UserModel(BaseModel):
    username: str
    email: str
    password: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetSettings(BaseSettings):
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30
