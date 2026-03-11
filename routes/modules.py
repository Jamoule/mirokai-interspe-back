import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from db import get_db, generate_id
from middleware.auth import admin_required

modules_bp = Blueprint("modules", __name__)

def module_to_dict(row):
    d = dict(row)
    if isinstance(d.get("image_urls"), str):
        try:
            d["image_urls"] = json.loads(d["image_urls"])
        except Exception:
            d["image_urls"] = []
    if isinstance(d.get("transcript_segments"), str):
        try:
            d["transcript_segments"] = json.loads(d["transcript_segments"])
        except Exception:
            d["transcript_segments"] = []
    d["has_quiz"] = bool(d.get("has_quiz"))
    d["is_active"] = bool(d.get("is_active"))
    return d

@modules_bp.route("", methods=["GET"])
def list_modules():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM modules WHERE is_active = 1 ORDER BY suggested_order"
    ).fetchall()
    conn.close()
    return jsonify([module_to_dict(r) for r in rows]), 200

@modules_bp.route("/all", methods=["GET"])
@admin_required
def list_all_modules():
    conn = get_db()
    rows = conn.execute("SELECT * FROM modules ORDER BY suggested_order").fetchall()
    conn.close()
    return jsonify([module_to_dict(r) for r in rows]), 200

@modules_bp.route("/qr/<string:qr_code>", methods=["GET"])
def get_by_qr(qr_code):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM modules WHERE qr_code = ? AND is_active = 1", (qr_code,)
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Module introuvable"}), 404
    return jsonify(module_to_dict(row)), 200

@modules_bp.route("/<string:module_id>", methods=["GET"])
def get_module(module_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Module introuvable"}), 404
    return jsonify(module_to_dict(row)), 200

@modules_bp.route("", methods=["POST"])
@admin_required
def create_module():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données requises"}), 400

    required = ["number", "name", "qr_code"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Champ requis: {field}"}), 400

    conn = get_db()
    existing_number = conn.execute("SELECT id FROM modules WHERE number = ?", (data["number"],)).fetchone()
    if existing_number:
        conn.close()
        return jsonify({"error": "Ce numéro de module est déjà pris"}), 400

    existing_qr = conn.execute("SELECT id FROM modules WHERE qr_code = ?", (data["qr_code"],)).fetchone()
    if existing_qr:
        conn.close()
        return jsonify({"error": "Ce QR code est déjà utilisé"}), 400

    module_id = generate_id()
    image_urls = json.dumps(data.get("image_urls", []))
    transcript_segments = json.dumps(data.get("transcript_segments", []))

    conn.execute(
        """INSERT INTO modules (id, number, name, description, media_type, media_url, image_urls,
           transcript_segments, qr_code, position_x, position_y, has_quiz, is_active, suggested_order)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            module_id, data["number"], data["name"],
            data.get("description"), data.get("media_type"), data.get("media_url"),
            image_urls, transcript_segments, data["qr_code"],
            data.get("position_x", 0.0), data.get("position_y", 0.0),
            1 if data.get("has_quiz") else 0,
            1 if data.get("is_active", True) else 0,
            data.get("suggested_order", data["number"])
        )
    )
    conn.commit()
    row = conn.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    conn.close()
    return jsonify(module_to_dict(row)), 201

@modules_bp.route("/<string:module_id>", methods=["PUT"])
@admin_required
def update_module(module_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données requises"}), 400

    conn = get_db()
    existing = conn.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Module introuvable"}), 404

    # Check unicity
    if "number" in data and data["number"] != existing["number"]:
        conflict = conn.execute("SELECT id FROM modules WHERE number = ? AND id != ?", (data["number"], module_id)).fetchone()
        if conflict:
            conn.close()
            return jsonify({"error": "Ce numéro de module est déjà pris"}), 400

    if "qr_code" in data and data["qr_code"] != existing["qr_code"]:
        conflict = conn.execute("SELECT id FROM modules WHERE qr_code = ? AND id != ?", (data["qr_code"], module_id)).fetchone()
        if conflict:
            conn.close()
            return jsonify({"error": "Ce QR code est déjà utilisé"}), 400

    fields = ["number", "name", "description", "media_type", "media_url", "qr_code",
              "position_x", "position_y", "has_quiz", "is_active", "suggested_order"]
    updates = []
    values = []
    for f in fields:
        if f in data:
            if f in ("has_quiz", "is_active"):
                updates.append(f"{f} = ?")
                values.append(1 if data[f] else 0)
            else:
                updates.append(f"{f} = ?")
                values.append(data[f])

    if "image_urls" in data:
        updates.append("image_urls = ?")
        values.append(json.dumps(data["image_urls"]))

    if "transcript_segments" in data:
        updates.append("transcript_segments = ?")
        values.append(json.dumps(data["transcript_segments"]))

    updates.append("updated_at = datetime('now')")
    values.append(module_id)

    conn.execute(f"UPDATE modules SET {', '.join(updates)} WHERE id = ?", values)
    conn.commit()
    row = conn.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    conn.close()
    return jsonify(module_to_dict(row)), 200

@modules_bp.route("/<string:module_id>/position", methods=["PATCH"])
@admin_required
def update_position(module_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données requises"}), 400

    conn = get_db()
    existing = conn.execute("SELECT id FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Module introuvable"}), 404

    conn.execute(
        "UPDATE modules SET position_x = ?, position_y = ?, updated_at = datetime('now') WHERE id = ?",
        (data.get("position_x", 0.0), data.get("position_y", 0.0), module_id)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    conn.close()
    return jsonify(module_to_dict(row)), 200

@modules_bp.route("/<string:module_id>/toggle", methods=["PATCH"])
@admin_required
def toggle_module(module_id):
    data = request.get_json()
    if not data or "is_active" not in data:
        return jsonify({"error": "is_active requis"}), 400

    conn = get_db()
    existing = conn.execute("SELECT id FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Module introuvable"}), 404

    conn.execute(
        "UPDATE modules SET is_active = ?, updated_at = datetime('now') WHERE id = ?",
        (1 if data["is_active"] else 0, module_id)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    conn.close()
    return jsonify(module_to_dict(row)), 200

@modules_bp.route("/<string:module_id>", methods=["DELETE"])
@admin_required
def delete_module(module_id):
    conn = get_db()
    existing = conn.execute("SELECT id FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Module introuvable"}), 404

    conn.execute("DELETE FROM modules WHERE id = ?", (module_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Module supprimé"}), 200
