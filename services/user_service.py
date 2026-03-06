from db.db_utils import get_db

def create_user_with_student(user_data):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, password, type, gender, birth_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data.get('first_name'),
            user_data.get('last_name'),
            user_data.get('email'),
            user_data.get('password'),
            user_data.get('type'),
            user_data.get('gender'),
            user_data.get('birth_date')
        ))
        user_id = cursor.lastrowid
        
        if user_data.get('type') == 'student':
            cursor.execute("INSERT INTO students (gpa, user_id) VALUES (?, ?)", (user_data.get('gpa', None), user_id))
        
        conn.commit()
        return user_id, user_data
