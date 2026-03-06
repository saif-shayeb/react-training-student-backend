from flask import Blueprint, request
from flask_jwt_extended import create_access_token, JWTManager
from db.db_utils import get_db
from utils.response_utils import success_response, error_response
from services.user_service import create_user_with_student
import os
from dotenv import load_dotenv

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def init_jwt(app):
    load_dotenv()
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
    jwt = JWTManager(app)
    return jwt

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
    
    if user:
        access_token = create_access_token(identity=str(user['id']), additional_claims={"type": user['type']})
        return success_response("Login successful", {"access_token": access_token})
    
    return error_response("Invalid email or password", 401)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        user_id, user_data = create_user_with_student(data)
        return success_response("User registered successfully", {"user_id": user_id}, 201)
    except Exception as e:
        return error_response(str(e), 500)
