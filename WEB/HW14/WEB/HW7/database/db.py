from colorama import init, Fore, Style
import configparser
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# f'postgresql://username:password@domain_name:port/database_name'
# url = f"postgresql://postgres:homework7@localhost:5432/homework7"

file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("DB", "user")
password = config.get("DB", "password")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

url = f"postgresql://{username}:{password}@{domain}:5433/{db_name}"


Base = declarative_base()

def session_db():
    engine = create_engine(url, echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    try:
        # Обработка подключения к базе данных для информативности (независимо от того, успешно ли подключение или нет)
        connection = engine.connect()
        print(Fore.LIGHTGREEN_EX + "Connection to the database successful." + Style.RESET_ALL)
        # connection.close()
    except Exception as e:
        print(Fore.RED + "Connection to the database failed:" + Style.RESET_ALL, e)

    return session

def async_session_db():
    async_engine = create_async_engine(url, echo=False)
    async_DBSession = sessionmaker(async_engine, class_=AsyncSession)
    async_session = async_DBSession()

    try:
        # Обработка подключения к базе данных для информативности (независимо от того, успешно ли подключение или нет)
        async_connection = async_engine.connect()
        print(Fore.LIGHTGREEN_EX + "Connection to the database successful." + Style.RESET_ALL)
        # connection.close()
    except Exception as e:
        print(Fore.RED + "Connection to the database failed:" + Style.RESET_ALL, e)

    return async_session



if __name__ == "__main__":
    print("Connection to bd...")


