import sqlite3
from contextlib import contextmanager
import os

DATABASE = 'database.db'

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query, params=(), commit=False):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return cursor.lastrowid
        return cursor.fetchall()
