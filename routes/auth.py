import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from db import get_db
from middleware.auth import admin_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email et mot de passe requis"}), 400

    conn = get_db()
    admin = conn.execute(
        "SELECT * FROM admins WHERE email = ? AND is_active = 1", (data["email"],)
    ).fetchone()

    if not admin or not bcrypt.checkpw(data["password"].encode(), admin["password_hash"].encode()):
        conn.close()
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401

    conn.execute(
        "UPDATE admins SET last_login_at = datetime('now') WHERE id = ?", (admin["id"],)
    )
    conn.commit()
    conn.close()

    token = create_access_token(identity=admin["id"])
    return jsonify({
        "token": token,
        "admin": {
            "id": admin["id"],
            "email": admin["email"],
            "display_name": admin["display_name"]
        }
    }), 200

@auth_bp.route("/me", methods=["GET"])
@admin_required
def me():
    admin_id = get_jwt_identity()
    conn = get_db()
    admin = conn.execute(
        "SELECT id, email, display_name, last_login_at FROM admins WHERE id = ?", (admin_id,)
    ).fetchone()
    conn.close()

    if not admin:
        return jsonify({"error": "Admin introuvable"}), 404

    return jsonify(dict(admin)), 200

@auth_bp.route("/logout", methods=["POST"])
@admin_required
def logout():
    return jsonify({"message": "Déconnecté"}), 200
