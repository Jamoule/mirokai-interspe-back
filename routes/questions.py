from flask import Blueprint, request, jsonify
from db import get_db, generate_id
from middleware.auth import admin_required

questions_bp = Blueprint("questions", __name__)

VALID_AGE_GROUPS = {"3-4", "5-7", "8-10", "parents"}

def question_with_answers(conn, question_id, include_secret=False):
    q = conn.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
    if not q:
        return None
    q_dict = dict(q)
    if not include_secret:
        q_dict.pop("secret_word", None)
    answers = conn.execute(
        "SELECT * FROM answers WHERE question_id = ? ORDER BY display_order", (question_id,)
    ).fetchall()
    q_dict["answers"] = [dict(a) for a in answers]
    return q_dict

@questions_bp.route("/modules/<string:module_id>/questions", methods=["GET"])
def get_questions(module_id):
    age_group = request.args.get("age_group")
    conn = get_db()

    module = conn.execute("SELECT id FROM modules WHERE id = ? AND is_active = 1", (module_id,)).fetchone()
    if not module:
        conn.close()
        return jsonify({"error": "Module introuvable"}), 404

    if age_group:
        rows = conn.execute(
            "SELECT id FROM questions WHERE module_id = ? AND age_group = ? ORDER BY display_order",
            (module_id, age_group)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id FROM questions WHERE module_id = ? ORDER BY display_order", (module_id,)
        ).fetchall()

    questions = [question_with_answers(conn, r["id"], include_secret=False) for r in rows]
    conn.close()
    return jsonify(questions), 200

@questions_bp.route("/modules/<string:module_id>/questions/all", methods=["GET"])
@admin_required
def get_all_questions(module_id):
    conn = get_db()
    module = conn.execute("SELECT id FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not module:
        conn.close()
        return jsonify({"error": "Module introuvable"}), 404

    rows = conn.execute(
        "SELECT id FROM questions WHERE module_id = ? ORDER BY age_group, display_order", (module_id,)
    ).fetchall()
    questions = [question_with_answers(conn, r["id"], include_secret=True) for r in rows]
    conn.close()
    return jsonify(questions), 200

@questions_bp.route("/questions", methods=["POST"])
@admin_required
def create_question():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données requises"}), 400

    required = ["module_id", "age_group", "question_text"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Champ requis: {field}"}), 400

    if data["age_group"] not in VALID_AGE_GROUPS:
        return jsonify({"error": f"age_group invalide. Valeurs: {', '.join(VALID_AGE_GROUPS)}"}), 400

    conn = get_db()
    module = conn.execute("SELECT id FROM modules WHERE id = ?", (data["module_id"],)).fetchone()
    if not module:
        conn.close()
        return jsonify({"error": "Module introuvable"}), 400

    q_id = generate_id()
    conn.execute(
        """INSERT INTO questions (id, module_id, age_group, question_text, secret_word, display_order)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (q_id, data["module_id"], data["age_group"], data["question_text"],
         data.get("secret_word"), data.get("display_order", 0))
    )

    for ans in data.get("answers", []):
        a_id = generate_id()
        conn.execute(
            "INSERT INTO answers (id, question_id, answer_text, is_correct, display_order) VALUES (?, ?, ?, ?, ?)",
            (a_id, q_id, ans["answer_text"], 1 if ans.get("is_correct") else 0, ans.get("display_order", 0))
        )

    conn.commit()
    result = question_with_answers(conn, q_id, include_secret=True)
    conn.close()
    return jsonify(result), 201

@questions_bp.route("/questions/<string:question_id>", methods=["PUT"])
@admin_required
def update_question(question_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données requises"}), 400

    conn = get_db()
    existing = conn.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Question introuvable"}), 404

    if "age_group" in data and data["age_group"] not in VALID_AGE_GROUPS:
        conn.close()
        return jsonify({"error": f"age_group invalide"}), 400

    fields = ["age_group", "question_text", "secret_word", "display_order"]
    updates = []
    values = []
    for f in fields:
        if f in data:
            updates.append(f"{f} = ?")
            values.append(data[f])

    if updates:
        values.append(question_id)
        conn.execute(f"UPDATE questions SET {', '.join(updates)} WHERE id = ?", values)

    if "answers" in data:
        conn.execute("DELETE FROM answers WHERE question_id = ?", (question_id,))
        for ans in data["answers"]:
            a_id = generate_id()
            conn.execute(
                "INSERT INTO answers (id, question_id, answer_text, is_correct, display_order) VALUES (?, ?, ?, ?, ?)",
                (a_id, question_id, ans["answer_text"], 1 if ans.get("is_correct") else 0, ans.get("display_order", 0))
            )

    conn.commit()
    result = question_with_answers(conn, question_id, include_secret=True)
    conn.close()
    return jsonify(result), 200

@questions_bp.route("/questions/<string:question_id>", methods=["DELETE"])
@admin_required
def delete_question(question_id):
    conn = get_db()
    existing = conn.execute("SELECT id FROM questions WHERE id = ?", (question_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Question introuvable"}), 404

    conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Question supprimée"}), 200
