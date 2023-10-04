from sqlalchemy import create_engine
from colorama import init, Fore, Style
import configparser
import pathlib

# Init colorama
init()

def test_connection():
    file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
    config = configparser.ConfigParser()
    config.read(file_config)

    username = config.get("DB", "user")
    password = config.get("DB", "password")
    db_name = config.get("DB", "db_name")
    domain = config.get("DB", "domain")

    url = f"postgresql://{username}:{password}@{domain}:5432/{db_name}"

    try:
        # Try connecting to the database
        engine = create_engine(url, echo=False)
        connection = engine.connect()
        connection.close()
        print(Fore.LIGHTGREEN_EX + "Connection to the database successful." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "Connection to the database failed:" + Style.RESET_ALL, e)


if __name__ == "__main__":
    print("Testing database connection...")
    test_connection()
