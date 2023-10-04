from connect import Base, engine
from datetime import date
from pydantic import BaseModel, field_validator, BaseConfig
from pydantic import BaseModel, field_validator, BaseConfig
from sqlalchemy import create_engine, Column, Integer, String, Date
from typing import List, Optional


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    birth_date = Column(Date)
    additional_info = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_info: Optional[str] = None


class ContactCreate(BaseModel):
    pass

    @field_validator("email", check_fields=False)
    def email_address_validator(cls, val):
        if not "@" in val:
            raise ValueError("Invalid email")
        return val


class ContactListResponse(BaseModel):
    contacts: List[ContactBase]

    class Config(BaseConfig):
        arbitrary_types_allowed = True
