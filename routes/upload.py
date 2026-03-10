import os
import uuid
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from middleware.auth import admin_required
from config import ALLOWED_EXTENSIONS

upload_bp = Blueprint("upload", __name__)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folder():
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    return folder

@upload_bp.route("", methods=["POST"])
@admin_required
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nom de fichier vide"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Type de fichier non autorisé"}), 400

    folder_param = request.args.get("folder", "uploads")
    # Sanitize folder name
    folder_param = "".join(c for c in folder_param if c.isalnum() or c in ("-", "_"))

    upload_dir = os.path.join(get_upload_folder(), folder_param)
    os.makedirs(upload_dir, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(upload_dir, unique_filename)
    file.save(filepath)

    # Return relative URL path
    url = f"/uploads/{folder_param}/{unique_filename}"
    return jsonify({"url": url, "filename": unique_filename}), 201

@upload_bp.route("", methods=["DELETE"])
@admin_required
def delete_file():
    data = request.get_json()
    if not data or not data.get("url"):
        return jsonify({"error": "URL requise"}), 400

    url = data["url"]
    # Expect url like /uploads/folder/filename.ext
    if not url.startswith("/uploads/"):
        return jsonify({"error": "URL invalide"}), 400

    relative_path = url[len("/uploads/"):]
    # Security: prevent path traversal
    relative_path = os.path.normpath(relative_path)
    if relative_path.startswith(".."):
        return jsonify({"error": "Chemin invalide"}), 400

    upload_base = get_upload_folder()
    filepath = os.path.join(upload_base, relative_path)

    if not os.path.exists(filepath):
        return jsonify({"error": "Fichier introuvable"}), 404

    os.remove(filepath)
    return jsonify({"message": "Fichier supprimé"}), 200
