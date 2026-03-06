import sqlite3;

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db_connection()
    with conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
               gpa REAL ,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) on DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                type TEXT NOT NULL ,
                birth_date DATE ,
                gender TEXT           
                           
            );  
        ''')
    conn.commit()
    conn.close()

def reset_db():
    conn = get_db_connection()
    with conn:
        conn.executescript('''
            DROP TABLE IF EXISTS students;
            DROP TABLE IF EXISTS users;
        ''')
    conn.commit()
    conn.close()
    init_db()