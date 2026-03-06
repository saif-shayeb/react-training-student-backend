from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from db.db_utils import get_db
from utils.response_utils import success_response, error_response

course_bp = Blueprint("courses", __name__, url_prefix="/courses")

@course_bp.route("/", methods=["GET"])
@jwt_required()
def get_courses():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM courses").fetchall()
    return jsonify([dict(row) for row in rows])

@course_bp.route("/", methods=["POST"])
@jwt_required()
def add_course():
    claims = get_jwt()
    if claims.get("type") != "admin":
        return error_response("Admin access required", 403)
    
    data = request.get_json()
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO courses (name, description, instructor, credits)
                VALUES (?, ?, ?, ?)
            """, (data.get("name"), data.get("description"), data.get("instructor"), data.get("credits", 3)))
            conn.commit()
            course_id = cursor.lastrowid
        return success_response("Course added successfully", {"id": course_id}, 201)
    except Exception as e:
        return error_response(str(e), 500)

@course_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_course(id):
    claims = get_jwt()
    if claims.get("type") != "admin":
        return error_response("Admin access required", 403)
    
    data = request.get_json()
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            res = cursor.execute("""
                UPDATE courses 
                SET name=?, description=?, instructor=?, credits=?
                WHERE id=?
            """, (data.get("name"), data.get("description"), data.get("instructor"), data.get("credits"), id))
            conn.commit()
            if res.rowcount == 0:
                return error_response("Course not found", 404)
        return success_response("Course updated successfully")
    except Exception as e:
        return error_response(str(e), 500)

@course_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_course(id):
    claims = get_jwt()
    if claims.get("type") != "admin":
        return error_response("Admin access required", 403)
    
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            res = cursor.execute("DELETE FROM courses WHERE id = ?", (id,))
            conn.commit()
            if res.rowcount == 0:
                return error_response("Course not found", 404)
        return success_response("Course deleted successfully")
    except Exception as e:
        return error_response(str(e), 500)

@course_bp.route("/enroll", methods=["POST"])
@jwt_required()
def enroll_course():
    user_id = get_jwt_identity()
    data = request.get_json()
    course_id = data.get("course_id")
    
    try:
        with get_db() as conn:
            # Get student_id from user_id
            student = conn.execute("SELECT id FROM students WHERE user_id = ?", (user_id,)).fetchone()
            if not student:
                return error_response("Student record not found", 404)
            
            student_id = student["id"]
            conn.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
            conn.commit()
        return success_response("Enrolled successfully")
    except Exception as e:
        return error_response("Already enrolled or error: " + str(e), 400)

@course_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_courses():
    user_id = get_jwt_identity()
    try:
        with get_db() as conn:
            rows = conn.execute("""
                SELECT c.* FROM courses c
                JOIN enrollments e ON c.id = e.course_id
                JOIN students s ON e.student_id = s.id
                WHERE s.user_id = ?
            """, (user_id,)).fetchall()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return error_response(str(e), 500)
