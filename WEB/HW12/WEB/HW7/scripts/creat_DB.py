import psycopg2
from psycopg2 import sql
import configparser
import pathlib

file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("DB", "user")
password = config.get("DB", "password")
db_name_new = config.get("DB", "db_name_new")
domain = config.get("DB", "domain")
port = 5433

connection = psycopg2.connect(user=username, password=password, host=domain, port=port, database="postgres")


def create_db():
    create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name_new))
    with connection.cursor() as cursor:
        cursor.execute(create_db_query)
        connection.commit()


if __name__ == "__main__":
    create_db()
    connection.close()
