from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import db.dbconn as dbconn
from routes.student_routes import student_bp
from routes.course_routes import course_bp
from routes.auth import auth_bp, init_jwt
import os

app = Flask(__name__, static_folder='../react-training-Students-manager/dist', static_url_path='/')
CORS(app)
dbconn.init_db()
init_jwt(app)

app.register_blueprint(student_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(course_bp)

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def serve(path):
    # Check if the requested path exists as a static file
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise, serve index.html for React Router to handle
    return send_from_directory(app.static_folder, 'index.html')

# Catch-all error handler for 404s to ensure index.html is served for SPA routes
@app.errorhandler(404)
def not_found(e):
    # Only return index.html for non-API requests
    if request.path.startswith('/students') or request.path.startswith('/auth'):
        return jsonify({"error": "Not Found"}), 404
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/hello")
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route("/reset", methods=["POST"])
def reset_database():
    try:
        dbconn.reset_db()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Database reset successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)