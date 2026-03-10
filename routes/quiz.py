from flask import Blueprint, request, jsonify
from db import get_db

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/validate", methods=["POST"])
def validate_answer():
    data = request.get_json()
    if not data or not data.get("question_id") or not data.get("answer_id"):
        return jsonify({"error": "question_id et answer_id requis"}), 400

    conn = get_db()
    answer = conn.execute(
        "SELECT * FROM answers WHERE id = ? AND question_id = ?",
        (data["answer_id"], data["question_id"])
    ).fetchone()

    if not answer:
        conn.close()
        return jsonify({"error": "Réponse introuvable pour cette question"}), 404

    if answer["is_correct"]:
        question = conn.execute(
            "SELECT secret_word FROM questions WHERE id = ?", (data["question_id"],)
        ).fetchone()
        conn.close()
        return jsonify({"correct": True, "secret_word": question["secret_word"] if question else None}), 200

    conn.close()
    return jsonify({"correct": False, "secret_word": None}), 200
