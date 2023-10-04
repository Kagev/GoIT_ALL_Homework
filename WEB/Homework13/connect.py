from pathlib import Path

import psycopg2
import os

from fastapi_mail import ConnectionConfig
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail

from config import setting

DATABASE_URL = f"postgresql://{setting.POSTGRES_USER}:{setting.POSTGRES_PASSWORD}@{setting.POSTGRES_HOST}:{setting.POSTGRES_PORT}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

conf = ConnectionConfig(
    MAIL_USERNAME=setting.MAIL_USERNAME,
    MAIL_PASSWORD=setting.MAIL_PASSWORD,
    MAIL_FROM=setting.MAIL_FROM,
    MAIL_PORT=setting.MAIL_PORT,
    MAIL_SERVER=setting.MAIL_SERVER,
    MAIL_FROM_NAME=setting.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_database_connection(POSTGRES_HOST, POSTGRES_NAME, POSTGRES_USER, POSTGRES_PASSWORD):
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_NAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


# Функция для выполнения SQL-запросов с возможностью получения результатов как словарей
def execute_query(query, params=None):
    conn = get_database_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
