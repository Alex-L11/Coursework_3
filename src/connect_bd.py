import psycopg2
from psycopg2 import IntegrityError, OperationalError, ProgrammingError
from psycopg2.extensions import connection


class DBConnector:
    """Производит подключение к базе данных и возвращает данные"""

    def __init__(self, db_config: dict) -> None:
        self._config = db_config
        self._conn = None

    def connect(self) -> connection:

        if self._conn is not None and not self._conn.closed:
            return self._conn
        else:
            conn = psycopg2.connect(**self._config)
            self._conn = conn

        return conn

    def execute(self, sql: str, params: tuple) -> None:
        conn = self.connect()

        with conn.cursor() as cursor:
            try:
                cursor.execute(sql, params)
                conn.commit()
            except ProgrammingError as e:
                conn.rollback()
                raise RuntimeError(f"Неверный SQL: {sql}. \n Ошибка: {e}") from e
            except IntegrityError as i:
                conn.rollback()
                raise RuntimeError(f"Нарушено ограничение базы: {i}") from i
            except OperationalError as o:
                conn.rollback()
                raise RuntimeError(f"Нарушено соединение с сервером: {o}") from o

    def fetch_all(self, sql: str, params: tuple = ()) -> list:
        conn = self.connect()

        with conn.cursor() as cursor:
            try:
                cursor.execute(sql, params)
                row = cursor.fetchall()
                conn.commit()
            except ProgrammingError as e:
                conn.rollback()
                raise RuntimeError(f"Неверный SQL: {sql}. \n Ошибка: {e}") from e
            except IntegrityError as i:
                conn.rollback()
                raise RuntimeError(f"Нарушено ограничение базы: {i}") from i
            except OperationalError as o:
                conn.rollback()
                raise RuntimeError(f"Нарушено соединение с сервером: {o}") from o

        return row

    def fetch_one(self, sql: str, params: tuple = ()) -> tuple | None:
        conn = self.connect()

        with conn.cursor() as cursor:
            try:
                cursor.execute(sql, params)
                table = cursor.fetchone()
                conn.commit()
            except ProgrammingError as e:
                conn.rollback()
                raise RuntimeError(f"Неверный SQL: {sql}. \n Ошибка: {e}") from e
            except IntegrityError as i:
                conn.rollback()
                raise RuntimeError(f"Нарушено ограничение базы: {i}") from i
            except OperationalError as o:
                conn.rollback()
                raise RuntimeError(f"Нарушено соединение с сервером: {o}") from o

        return table
