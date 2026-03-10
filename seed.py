import bcrypt
import json
from db import get_db, generate_id, init_db

def seed():
    init_db()
    conn = get_db()

    # Admin par défaut
    existing = conn.execute("SELECT id FROM admins WHERE email = ?", ("admin@mirokai.fr",)).fetchone()
    if not existing:
        admin_id = generate_id()
        password_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        conn.execute(
            "INSERT INTO admins (id, email, password_hash, display_name) VALUES (?, ?, ?, ?)",
            (admin_id, "admin@mirokai.fr", password_hash, "Administrateur")
        )
        print("Admin créé : admin@mirokai.fr / admin123")

    # Parcours settings par défaut
    existing_settings = conn.execute("SELECT id FROM parcours_settings WHERE is_active = 1").fetchone()
    if not existing_settings:
        settings_id = generate_id()
        conn.execute(
            """INSERT INTO parcours_settings (id, parcours_name, welcome_message, completion_message,
               completion_email_template, estimated_duration_min)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (settings_id, "Parcours Mirokai",
             "Bienvenue dans l'aventure Mirokai !",
             "Félicitations, vous avez terminé le parcours !",
             "Merci de votre visite ! Voici un petit souvenir de votre aventure sur Nimira.",
             35)
        )
        print("Parcours settings créés.")

    # Module exemple
    existing_module = conn.execute("SELECT id FROM modules WHERE number = ?", (1,)).fetchone()
    if not existing_module:
        module_id = generate_id()
        conn.execute(
            """INSERT INTO modules (id, number, name, description, media_type, qr_code, has_quiz, is_active, suggested_order, image_urls)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (module_id, 1, "La Planète Nimira", "Découvrez la planète Nimira et ses habitants.",
             "image", "MOD-001", 1, 1, 1, "[]")
        )

        # Question exemple
        q_id = generate_id()
        conn.execute(
            """INSERT INTO questions (id, module_id, age_group, question_text, secret_word, display_order)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (q_id, module_id, "5-7", "Comment s'appelle la planète ?", "NIMIRA", 1)
        )

        # Réponses
        answers = [
            (generate_id(), q_id, "Nimira", 1, 1),
            (generate_id(), q_id, "Pandora", 0, 2),
            (generate_id(), q_id, "Mirania", 0, 3),
        ]
        for a in answers:
            conn.execute(
                "INSERT INTO answers (id, question_id, answer_text, is_correct, display_order) VALUES (?, ?, ?, ?, ?)",
                a
            )
        print("Module exemple créé.")

    conn.commit()
    conn.close()
    print("Seed terminé.")

if __name__ == "__main__":
    seed()
