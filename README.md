# Mirokai API — Back-end

API back-end du parcours interactif Mirokai. Gère les modules de contenu, les quiz adaptatifs par tranche d'âge, l'upload de médias et l'administration du parcours.

**Stack** : Flask 3.1 · SQLite · JWT (flask-jwt-extended) · bcrypt

---

## Prérequis

| Outil      | Version minimale | Vérification         |
| ---------- | ---------------- | -------------------- |
| **Python** | 3.10+            | `python3 --version`  |
| **pip**    | Inclus avec Python | `pip3 --version`   |

SQLite est intégré à Python, aucune base externe n'est requise.

---

## Installation

```bash
# 1. Se placer dans le dossier
cd api

# 2. Environnement virtuel
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Dépendances
pip install -r requirements.txt

# 4. Variables d'environnement
cp .env.example .env
# Éditer .env pour renseigner les clés secrètes en production
```

---

## Variables d'environnement

Définis dans `.env` (voir `.env.example`) :

| Variable             | Défaut              | Description                          |
| -------------------- | ------------------- | ------------------------------------ |
| `SECRET_KEY`         | `dev-secret-key`    | Clé secrète Flask                    |
| `JWT_SECRET_KEY`     | `dev-jwt-secret`    | Clé de signature des tokens JWT      |
| `DATABASE_PATH`      | `./mirokai.db`      | Chemin vers la base SQLite           |
| `UPLOAD_FOLDER`      | `./uploads`          | Répertoire de stockage des médias   |
| `MAX_CONTENT_LENGTH` | `104857600` (100 Mo) | Taille max d'upload                 |

---

## Lancement

```bash
# Seed : crée les tables + un admin par défaut + données de démo
python seed.py            # première fois
python seed.py --reset    # recrée les modules de démo (efface les existants)

# Serveur de dev avec auto-reload
flask run --port 5000 --debug
# ou
python app.py
```

L'API est alors accessible sur `http://localhost:5000`.

**Compte admin par défaut** : `admin@mirokai.fr` / `admin123`

---

## Structure du projet

```
api/
├── app.py                  # Point d'entrée, factory create_app()
├── config.py               # Lecture du .env, constantes
├── db.py                   # Connexion SQLite, init_db()
├── schema.sql              # Schéma de la base de données
├── seed.py                 # Seeding admin + modules + settings
├── requirements.txt
├── .env.example
│
├── middleware/
│   └── auth.py             # Décorateur @admin_required (JWT + is_active)
│
├── routes/
│   ├── auth.py             # Login / me / logout
│   ├── admins.py           # CRUD administrateurs
│   ├── modules.py          # CRUD modules de contenu
│   ├── questions.py        # CRUD questions & réponses
│   ├── quiz.py             # Validation des réponses au quiz
│   ├── upload.py           # Upload / suppression de fichiers
│   └── settings.py         # Paramètres du parcours
│
└── uploads/                # Stockage local des médias (images, vidéo, audio)
```

---

## Base de données

SQLite avec 5 tables. Le schéma complet est dans `schema.sql`.

### `admins`
Comptes administrateurs du back-office.

| Colonne         | Type | Notes                          |
| --------------- | ---- | ------------------------------ |
| `id`            | TEXT | PK (UUID)                      |
| `email`         | TEXT | Unique                         |
| `password_hash` | TEXT | Hash bcrypt                    |
| `display_name`  | TEXT |                                |
| `is_active`     | INT  | 1 = actif, 0 = désactivé      |
| `last_login_at` | TEXT | Mis à jour à chaque login      |
| `created_at`    | TEXT |                                |

### `modules`
Contenus du parcours (étapes avec média, QR code, position sur le plan).

| Colonne              | Type | Notes                              |
| -------------------- | ---- | ---------------------------------- |
| `id`                 | TEXT | PK (UUID)                          |
| `number`             | INT  | Unique, numéro d'étape             |
| `name`               | TEXT |                                    |
| `description`        | TEXT |                                    |
| `media_type`         | TEXT | `video`, `audio`, `image`…         |
| `media_url`          | TEXT |                                    |
| `image_urls`         | TEXT | JSON array                         |
| `transcript_segments`| TEXT | JSON array (sous-titres horodatés) |
| `qr_code`            | TEXT | Unique, identifiant QR             |
| `position_x/y`       | REAL | Position sur le plan du parcours   |
| `has_quiz`           | INT  | 1 = quiz associé                   |
| `is_active`          | INT  | 1 = visible côté visiteur          |
| `suggested_order`    | INT  | Ordre de visite recommandé         |

### `questions`
Questions de quiz rattachées à un module, filtrées par tranche d'âge.

| Colonne        | Type | Notes                                        |
| -------------- | ---- | -------------------------------------------- |
| `id`           | TEXT | PK (UUID)                                    |
| `module_id`    | TEXT | FK → modules (CASCADE)                       |
| `age_group`    | TEXT | `5-7`, `8-10`, `11-13`, `14+`, `all`         |
| `question_text`| TEXT |                                              |
| `secret_word`  | TEXT | Révélé uniquement si bonne réponse           |
| `display_order`| INT  |                                              |

### `answers`
Réponses possibles pour chaque question.

| Colonne        | Type | Notes                    |
| -------------- | ---- | ------------------------ |
| `id`           | TEXT | PK (UUID)                |
| `question_id`  | TEXT | FK → questions (CASCADE) |
| `answer_text`  | TEXT |                          |
| `is_correct`   | INT  | 1 = bonne réponse        |
| `display_order`| INT  |                          |

### `parcours_settings`
Configuration globale du parcours (singleton).

| Colonne                     | Type | Notes                       |
| --------------------------- | ---- | --------------------------- |
| `id`                        | TEXT | PK (UUID)                   |
| `parcours_name`             | TEXT | Nom affiché                 |
| `plan_image_url`            | TEXT | Image du plan               |
| `welcome_message`           | TEXT |                             |
| `completion_message`        | TEXT | Message de fin de parcours  |
| `completion_email_template` | TEXT |                             |
| `completion_redirect_url`   | TEXT |                             |
| `estimated_duration_min`    | INT  | Durée estimée en minutes    |
| `is_active`                 | INT  |                             |

---

## API — Routes

Toutes les routes sont préfixées par `/api`.
Les routes marquées **Auth** nécessitent le header `Authorization: Bearer <token>`.

### Authentification — `/api/auth`

| Méthode | Route    | Auth | Description                                 |
| ------- | -------- | ---- | ------------------------------------------- |
| POST    | `/login` | —    | Login email/password → JWT + infos admin    |
| GET     | `/me`    | Oui  | Infos de l'admin connecté                   |
| POST    | `/logout`| Oui  | Déconnexion                                 |

### Administrateurs — `/api/admins`

| Méthode | Route          | Auth | Description                                        |
| ------- | -------------- | ---- | -------------------------------------------------- |
| GET     | `/`            | Oui  | Liste des admins                                   |
| POST    | `/`            | Oui  | Créer un admin (email, password, display_name)     |
| PUT     | `/<admin_id>`  | Oui  | Modifier un admin                                  |
| DELETE  | `/<admin_id>`  | Oui  | Supprimer (interdit sur soi-même / dernier actif)  |

### Modules — `/api/modules`

| Méthode | Route                  | Auth | Description                               |
| ------- | ---------------------- | ---- | ----------------------------------------- |
| GET     | `/`                    | —    | Modules actifs (ordonnés)                 |
| GET     | `/all`                 | Oui  | Tous les modules (admin)                  |
| GET     | `/qr/<qr_code>`       | —    | Module par QR code (+ `next_module_id`)   |
| GET     | `/<module_id>`         | —    | Module par ID (+ `next_module_id`)        |
| POST    | `/`                    | Oui  | Créer un module                           |
| PUT     | `/<module_id>`         | Oui  | Modifier un module                        |
| PATCH   | `/<module_id>/position`| Oui  | Modifier la position sur le plan          |
| PATCH   | `/positions`           | Oui  | Mise à jour groupée des positions         |
| PATCH   | `/<module_id>/toggle`  | Oui  | Activer / désactiver un module            |
| DELETE  | `/<module_id>`         | Oui  | Supprimer un module                       |

### Questions — `/api`

| Méthode | Route                              | Auth | Description                          |
| ------- | ---------------------------------- | ---- | ------------------------------------ |
| GET     | `/modules/<id>/questions`          | —    | Questions par module et `age_group`  |
| GET     | `/modules/<id>/questions/all`      | Oui  | Toutes les questions d'un module     |
| POST    | `/questions`                       | Oui  | Créer question + réponses            |
| PUT     | `/questions/<question_id>`         | Oui  | Modifier question + réponses         |
| DELETE  | `/questions/<question_id>`         | Oui  | Supprimer une question               |

### Quiz — `/api/quiz`

| Méthode | Route       | Auth | Description                                         |
| ------- | ----------- | ---- | --------------------------------------------------- |
| POST    | `/validate` | —    | Valider une réponse → `correct` + `secret_word`     |

### Upload — `/api/upload`

| Méthode | Route | Auth | Description                                                    |
| ------- | ----- | ---- | -------------------------------------------------------------- |
| POST    | `/`   | Oui  | Upload fichier (form-data `file`, query param `folder`)        |
| DELETE  | `/`   | Oui  | Supprimer un fichier par son URL                               |

Formats acceptés : `png`, `jpg`, `jpeg`, `gif`, `webp`, `mp4`, `webm`, `mp3`, `wav`, `ogg`, `m4a`.

### Paramètres du parcours — `/api/settings`

| Méthode | Route | Auth | Description                              |
| ------- | ----- | ---- | ---------------------------------------- |
| GET     | `/`   | —    | Récupérer les paramètres du parcours     |
| PUT     | `/`   | Oui  | Créer ou modifier les paramètres         |

### Fichiers statiques

| Méthode | Route                      | Auth | Description           |
| ------- | -------------------------- | ---- | --------------------- |
| GET     | `/uploads/<path:filename>` | —    | Servir un fichier uploadé |

---

## Authentification

L'API utilise **JWT** via `flask-jwt-extended`.

1. Appeler `POST /api/auth/login` avec `{ "email": "...", "password": "..." }`.
2. Le serveur retourne un `access_token`.
3. Inclure le token dans les requêtes protégées : `Authorization: Bearer <access_token>`.

Le décorateur `@admin_required` (dans `middleware/auth.py`) vérifie le JWT **et** que l'admin est actif (`is_active = 1`). Retourne 401 si token invalide, 403 si admin désactivé.

---

## Règles métier

- **Modules** : le champ `number` et `qr_code` sont uniques. `suggested_order` détermine l'enchaînement des modules (`next_module_id` est calculé dynamiquement).
- **Questions** : filtrées par `age_group` (`5-7`, `8-10`, `11-13`, `14+`, `all`). Le `secret_word` n'est révélé au visiteur que si sa réponse est correcte.
- **Admins** : un admin ne peut pas se supprimer lui-même ni supprimer/désactiver le dernier admin actif.
- **Uploads** : les noms de fichiers sont rendus uniques via UUID, protection contre le path traversal, sous-dossiers optionnels.

---

## CORS

Origines autorisées (configurées dans `app.py`) :

- `http://localhost:5173` (Vite dev)
- `http://localhost:3000`
- `https://mirokai-interspe-front.vercel.app` (production)

---

## Dépendances

Listées dans `requirements.txt` :

| Package              | Rôle                                  |
| -------------------- | ------------------------------------- |
| `flask`              | Framework web                         |
| `flask-cors`         | Gestion du CORS                       |
| `flask-jwt-extended` | Authentification JWT                  |
| `bcrypt`             | Hachage des mots de passe             |
| `python-dotenv`      | Chargement des variables `.env`       |
