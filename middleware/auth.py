from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from db import get_db

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return jsonify({"error": "Token invalide ou manquant"}), 401

        admin_id = get_jwt_identity()
        conn = get_db()
        admin = conn.execute(
            "SELECT id, email, display_name, is_active FROM admins WHERE id = ?", (admin_id,)
        ).fetchone()
        conn.close()

        if not admin or not admin["is_active"]:
            return jsonify({"error": "Accès refusé"}), 403

        return f(*args, **kwargs)
    return decorated
