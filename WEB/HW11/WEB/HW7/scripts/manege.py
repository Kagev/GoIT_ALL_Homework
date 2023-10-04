"""
фиксаю проблему с удаленным файлом версии  миграции через "DROP TABLE alembic_version;"
подсмотрено на stackoverflow, chatGPT  ище пару ресурсов

"""

from sqlalchemy import text
from database.db import session_db


def drop_alembic_version_table():
    session = session_db()

    try:
        # SQL-запрос для удаления таблицы alembic_version
        drop_table_query = text("DROP TABLE IF EXISTS alembic_version;")
        session.execute(drop_table_query)
        session.commit()

        print("Таблица alembic_version успешно удалена.")
    except Exception as e:
        print("Ошибка при выполнении запроса:", e)
        session.rollback()
    finally:
        # Закрываем сессию
        session.close()

if __name__ == "__main__":
    drop_alembic_version_table()
