import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import config
from db import init_db

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH
    app.config["UPLOAD_FOLDER"] = os.path.abspath(config.UPLOAD_FOLDER)

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://localhost:3000"]}},
         allow_headers=["Authorization", "Content-Type"])

    JWTManager(app)

    # Servir les fichiers uploadés
    @app.route("/uploads/<path:filename>")
    def serve_upload(filename):
        upload_dir = app.config["UPLOAD_FOLDER"]
        # Security: prevent path traversal
        safe_path = os.path.normpath(filename)
        if safe_path.startswith(".."):
            return jsonify({"error": "Accès interdit"}), 403
        directory = os.path.dirname(os.path.join(upload_dir, safe_path))
        basename = os.path.basename(safe_path)
        return send_from_directory(directory, basename)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.modules import modules_bp
    from routes.questions import questions_bp
    from routes.quiz import quiz_bp
    from routes.upload import upload_bp
    from routes.settings import settings_bp
    from routes.admins import admins_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(modules_bp, url_prefix="/api/modules")
    app.register_blueprint(questions_bp, url_prefix="/api")
    app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(settings_bp, url_prefix="/api/settings")
    app.register_blueprint(admins_bp, url_prefix="/api/admins")

    # Error handlers
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "Non authentifié"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "Accès interdit"}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Ressource introuvable"}), 404

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"error": "Fichier trop volumineux"}), 413

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Erreur serveur"}), 500

    # Init DB on startup
    with app.app_context():
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        init_db()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
