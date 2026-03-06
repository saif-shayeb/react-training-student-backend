import sqlite3
import os

DATABASE = 'database.db'

def test_cascade():
    # Connect and enable FK
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row

    try:
        # Insert a test user
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name, email, password, type) VALUES ('Test', 'User', 'test_delete@example.com', 'pass', 'student')")
        user_id = cursor.lastrowid

        # Insert a test student
        cursor.execute("INSERT INTO students (gpa, user_id) VALUES (3.5, ?)", (user_id,))
        student_id = cursor.lastrowid
        conn.commit()

        # Verify both exist
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        student = conn.execute("SELECT * FROM students WHERE user_id = ?", (user_id,)).fetchone()
        print(f"User exists: {user is not None}")
        print(f"Student exists: {student is not None}")

        if not user or not student:
            print("Setup failed!")
            return

        # Delete user
        print(f"Deleting user {user_id}...")
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        # Verify student is gone
        student = conn.execute("SELECT * FROM students WHERE user_id = ?", (user_id,)).fetchone()
        if student is None:
            print("SUCCESS: Student record was automatically deleted (Cascade working).")
        else:
            print("FAILURE: Student record still exists (Cascade NOT working).")

    finally:
        # Cleanup
        conn.execute("DELETE FROM users WHERE email = 'test_delete@example.com'")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    if os.path.exists(DATABASE):
        test_cascade()
    else:
        print(f"Database {DATABASE} not found.")
