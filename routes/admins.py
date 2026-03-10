import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from db import get_db, generate_id
from middleware.auth import admin_required

admins_bp = Blueprint("admins", __name__)

def admin_to_dict(row):
    d = dict(row)
    d.pop("password_hash", None)
    d["is_active"] = bool(d.get("is_active"))
    return d

@admins_bp.route("", methods=["GET"])
@admin_required
def list_admins():
    conn = get_db()
    rows = conn.execute("SELECT * FROM admins ORDER BY created_at").fetchall()
    conn.close()
    return jsonify([admin_to_dict(r) for r in rows]), 200

@admins_bp.route("", methods=["POST"])
@admin_required
def create_admin():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données requises"}), 400

    required = ["email", "password", "display_name"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Champ requis: {field}"}), 400

    conn = get_db()
    existing = conn.execute("SELECT id FROM admins WHERE email = ?", (data["email"],)).fetchone()
    if existing:
        conn.close()
        return jsonify({"error": "Cet email est déjà utilisé"}), 400

    admin_id = generate_id()
    password_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
    conn.execute(
        "INSERT INTO admins (id, email, password_hash, display_name) VALUES (?, ?, ?, ?)",
        (admin_id, data["email"], password_hash, data["display_name"])
    )
    conn.commit()
    row = conn.execute("SELECT * FROM admins WHERE id = ?", (admin_id,)).fetchone()
    conn.close()
    return jsonify(admin_to_dict(row)), 201

@admins_bp.route("/<string:admin_id>", methods=["PUT"])
@admin_required
def update_admin(admin_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données requises"}), 400

    current_admin_id = get_jwt_identity()
    conn = get_db()
    existing = conn.execute("SELECT * FROM admins WHERE id = ?", (admin_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Admin introuvable"}), 404

    # Un admin ne peut pas se désactiver lui-même
    if "is_active" in data and not data["is_active"] and admin_id == current_admin_id:
        conn.close()
        return jsonify({"error": "Vous ne pouvez pas vous désactiver vous-même"}), 400

    updates = []
    values = []

    if "email" in data and data["email"] != existing["email"]:
        conflict = conn.execute("SELECT id FROM admins WHERE email = ? AND id != ?", (data["email"], admin_id)).fetchone()
        if conflict:
            conn.close()
            return jsonify({"error": "Cet email est déjà utilisé"}), 400
        updates.append("email = ?")
        values.append(data["email"])

    if "display_name" in data:
        updates.append("display_name = ?")
        values.append(data["display_name"])

    if "password" in data:
        password_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
        updates.append("password_hash = ?")
        values.append(password_hash)

    if "is_active" in data:
        updates.append("is_active = ?")
        values.append(1 if data["is_active"] else 0)

    if updates:
        values.append(admin_id)
        conn.execute(f"UPDATE admins SET {', '.join(updates)} WHERE id = ?", values)
        conn.commit()

    row = conn.execute("SELECT * FROM admins WHERE id = ?", (admin_id,)).fetchone()
    conn.close()
    return jsonify(admin_to_dict(row)), 200

@admins_bp.route("/<string:admin_id>", methods=["DELETE"])
@admin_required
def delete_admin(admin_id):
    current_admin_id = get_jwt_identity()

    if admin_id == current_admin_id:
        return jsonify({"error": "Vous ne pouvez pas vous supprimer vous-même"}), 400

    conn = get_db()
    existing = conn.execute("SELECT id FROM admins WHERE id = ?", (admin_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Admin introuvable"}), 404

    active_count = conn.execute("SELECT COUNT(*) as cnt FROM admins WHERE is_active = 1").fetchone()["cnt"]
    target = conn.execute("SELECT is_active FROM admins WHERE id = ?", (admin_id,)).fetchone()
    if target["is_active"] and active_count <= 1:
        conn.close()
        return jsonify({"error": "Impossible de supprimer le dernier admin actif"}), 400

    conn.execute("DELETE FROM admins WHERE id = ?", (admin_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Admin supprimé"}), 200
