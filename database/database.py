import threading
import sqlite3
import os
import settings

TABLES_PATH = os.path.join(settings.ROOT_DIRPATH, "database/tables.sql")
DATABASE_PATH = os.path.join(settings.ROOT_DIRPATH, "data.db")


class Database:
    lock = threading.Lock()
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = true;")
    with open(TABLES_PATH) as f:
        cursor.executescript(f.read())

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.lock.release()

    def insert(self, query: str):
        try:
            self.cursor.execute(query)
            return self.cursor.lastrowid
        except Exception as e:
            logger.debug(query)
            logger.exception(e)
            raise

    def select(self, query: str):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            logger.debug(query)
            logger.exception(e)
            raise

    def update(self, query: str):
        try:
            self.cursor.execute(query)
        except Exception as e:
            logger.debug(query)
            logger.exception(e)
            raise


logger = settings.logmaker(__name__)
