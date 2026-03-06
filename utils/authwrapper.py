from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("type") != required_role:
                return jsonify({"error": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
