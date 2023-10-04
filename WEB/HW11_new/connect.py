import psycopg2
import os
import configparser
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

current_directory = os.path.dirname(os.path.abspath(__file__))

# Полный путь к файлу settings_connect.ini
config_file_path = os.path.join(current_directory, 'settings_connect.ini')

if os.path.exists(config_file_path):
    config = configparser.ConfigParser()
    config.read(config_file_path)

    db_config = config['DB']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_name = db_config['NAME']
    db_host = db_config['HOST']
    db_port = db_config['PORT']
else:
    print("Файл settings_connect.ini не найден в текущей директории.")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# инициализации подключения к базе данных
def get_database_connection():
    return psycopg2.connect(
        host="localhost",
        database="fast_connection",
        user="postgres",
        password="fast_connection",
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
