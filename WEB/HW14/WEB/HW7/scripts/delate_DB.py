from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database.db import url


engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    try:
        clear_sql = text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        session.execute(clear_sql)
        session.commit()
        print("Database cleared successfully.")
    except Exception as e:
        session.rollback()
        print("An error occurred:", e)
    finally:
        session.close()