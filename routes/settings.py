from flask import Blueprint, request, jsonify
from db import get_db, generate_id
from middleware.auth import admin_required

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("", methods=["GET"])
def get_settings():
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM parcours_settings WHERE is_active = 1 LIMIT 1"
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Paramètres introuvables"}), 404
    return jsonify(dict(row)), 200

@settings_bp.route("", methods=["PUT"])
@admin_required
def update_settings():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données requises"}), 400

    conn = get_db()
    existing = conn.execute("SELECT * FROM parcours_settings WHERE is_active = 1 LIMIT 1").fetchone()

    if not existing:
        # Créer les settings s'ils n'existent pas
        settings_id = generate_id()
        conn.execute(
            """INSERT INTO parcours_settings (id, parcours_name, plan_image_url, welcome_message,
               completion_message, completion_email_template, completion_redirect_url, estimated_duration_min)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (settings_id,
             data.get("parcours_name", "Parcours Mirokai"),
             data.get("plan_image_url"),
             data.get("welcome_message"),
             data.get("completion_message"),
             data.get("completion_email_template"),
             data.get("completion_redirect_url"),
             data.get("estimated_duration_min", 30))
        )
        conn.commit()
        row = conn.execute("SELECT * FROM parcours_settings WHERE id = ?", (settings_id,)).fetchone()
        conn.close()
        return jsonify(dict(row)), 201

    fields = ["parcours_name", "plan_image_url", "welcome_message", "completion_message",
              "completion_email_template", "completion_redirect_url", "estimated_duration_min"]
    updates = []
    values = []
    for f in fields:
        if f in data:
            updates.append(f"{f} = ?")
            values.append(data[f])

    updates.append("updated_at = datetime('now')")
    values.append(existing["id"])

    conn.execute(f"UPDATE parcours_settings SET {', '.join(updates)} WHERE id = ?", values)
    conn.commit()
    row = conn.execute("SELECT * FROM parcours_settings WHERE id = ?", (existing["id"],)).fetchone()
    conn.close()
    return jsonify(dict(row)), 200
