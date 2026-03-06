from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from db.db_utils import get_db
from utils.response_utils import success_response, error_response
from services.user_service import create_user_with_student

student_bp = Blueprint("students", __name__, url_prefix="/students")

@student_bp.route("/", methods=["GET"])
@jwt_required()
def get_students():
    claims = get_jwt()
    user_id = get_jwt_identity()
    with get_db() as conn:
        if claims.get("type") == "admin":
            rows = conn.execute("""
                SELECT users.*, students.gpa FROM students
                JOIN users ON students.user_id = users.id
            """).fetchall()
        else:
            rows = conn.execute("""
                SELECT users.*, students.gpa FROM students
                JOIN users ON students.user_id = users.id
                WHERE users.id = ?
            """, (user_id,)).fetchall()
    return jsonify([dict(row) for row in rows])

@student_bp.route("/", methods=["POST"])
def add_student():
    data = request.get_json()
    try:
        user_id, user_data = create_user_with_student(data)
        return success_response("Student added successfully", {"user_id": user_id}, 201)
    except Exception as e:
        return error_response(str(e), 500)

@student_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            res = cursor.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
            count = res.rowcount
        return success_response("Student deleted successfully" if count > 0 else "Student not found")
    except Exception as e:
        return error_response(str(e), 500)

@student_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            res = cursor.execute("""
                UPDATE users 
                SET first_name=?, last_name=?, email=?, password=?, gender=?, birth_date=?
                WHERE id=?
            """, (
                data.get("first_name"), 
                data.get("last_name"), 
                data.get("email"), 
                data.get("password"),
                data.get("gender"),
                data.get("birth_date"),
                id
            ))
            if res.rowcount == 0:
                return error_response("Student not found", 404)
            cursor.execute("UPDATE students SET gpa=? WHERE user_id=?", (data.get("gpa"), id))
            conn.commit()
        return success_response("Student updated successfully")
    except Exception as e:
        return error_response(str(e), 500)