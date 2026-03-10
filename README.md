# Mirokai API

API back-end du parcours Mirokai. Construite avec Flask + SQLite + JWT. Les médias sont stockés localement.

---

## Prérequis

| Outil | Version minimale | Vérification |
|---|---|---|
| Python | 3.10+ | `python3 --version` |
| pip | inclus avec Python | `pip3 --version` |

> Aucune base de données externe requise — SQLite est intégré à Python.

---

## Installation

### 1. Cloner / se placer dans le dossier

```bash
cd /home/jipei/projects/mirokai-back/api
```

### 2. Créer l'environnement virtuel

```bash
python3 -m venv venv
```

### 3. Activer l'environnement virtuel

```bash
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

> Le prompt doit afficher `(venv)` pour confirmer l'activation.

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Editer `.env` :

```env
SECRET_KEY=une-cle-secrete-robuste
JWT_SECRET_KEY=une-autre-cle-jwt-robuste
DATABASE_PATH=./mirokai.db
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=104857600
```

> `MAX_CONTENT_LENGTH` est en octets. `104857600` = 100 Mo.

### 6. Initialiser la base de données et les données de démo

```bash
python seed.py
```

Ce script :
- Crée toutes les tables SQLite (`mirokai.db`)
- Crée un admin par défaut
- Insère un module et une question d'exemple

**Identifiants admin créés :**

```
Email    : admin@mirokai.fr
Password : admin123
```

> Changer ce mot de passe en production via `PUT /api/admins/:id`.

---

## Lancer le serveur

```bash
# Mode développement (hot reload)
flask run --port 5000 --debug

# Ou directement
python app.py
```

L'API est accessible sur : `http://localhost:5000`

---

## Structure du projet

```
api/
├── app.py              # Point d'entrée Flask, config, CORS, blueprints
├── config.py           # Lecture des variables d'environnement
├── db.py               # Connexion SQLite, helpers (get_db, generate_id, init_db)
├── seed.py             # Initialisation BDD + données de démo
├── schema.sql          # Définition des tables SQL
├── requirements.txt    # Dépendances Python
├── .env                # Variables d'environnement (non versionné)
├── .env.example        # Template des variables d'environnement
├── mirokai.db          # Base de données SQLite (générée, non versionné)
│
├── routes/
│   ├── auth.py         # /api/auth — login, logout, me
│   ├── modules.py      # /api/modules — CRUD modules
│   ├── questions.py    # /api/modules/:id/questions — CRUD questions
│   ├── quiz.py         # /api/quiz/validate — validation réponse
│   ├── upload.py       # /api/upload — upload/suppression fichiers locaux
│   ├── settings.py     # /api/settings — config du parcours
│   └── admins.py       # /api/admins — CRUD admins
│
├── middleware/
│   └── auth.py         # Décorateur @admin_required (vérification JWT)
│
└── uploads/            # Médias uploadés (non versionné)
    ├── images/
    ├── videos/
    └── audioguides/
```

---

## Endpoints

### Auth

| Méthode | Route | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/login` | Non | Connexion admin |
| POST | `/api/auth/logout` | Admin | Déconnexion |
| GET | `/api/auth/me` | Admin | Profil admin connecté |

### Modules

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/api/modules` | Non | Liste des modules actifs |
| GET | `/api/modules/all` | Admin | Tous les modules |
| GET | `/api/modules/:id` | Non | Détail d'un module |
| GET | `/api/modules/qr/:qr_code` | Non | Module par QR code |
| POST | `/api/modules` | Admin | Créer un module |
| PUT | `/api/modules/:id` | Admin | Modifier un module |
| PATCH | `/api/modules/:id/position` | Admin | Mettre à jour la position |
| PATCH | `/api/modules/:id/toggle` | Admin | Activer / désactiver |
| DELETE | `/api/modules/:id` | Admin | Supprimer un module |

### Questions

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/api/modules/:id/questions` | Non | Questions par tranche d'âge |
| GET | `/api/modules/:id/questions/all` | Admin | Toutes les questions |
| POST | `/api/questions` | Admin | Créer une question |
| PUT | `/api/questions/:id` | Admin | Modifier une question |
| DELETE | `/api/questions/:id` | Admin | Supprimer une question |

### Quiz

| Méthode | Route | Auth | Description |
|---|---|---|---|
| POST | `/api/quiz/validate` | Non | Valider une réponse → mot secret |

### Upload

| Méthode | Route | Auth | Description |
|---|---|---|---|
| POST | `/api/upload` | Admin | Uploader un fichier |
| DELETE | `/api/upload` | Admin | Supprimer un fichier |

Les fichiers sont servis via : `GET /uploads/<dossier>/<fichier>`

### Settings

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/api/settings` | Non | Config du parcours |
| PUT | `/api/settings` | Admin | Modifier la config |

### Admins

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/api/admins` | Admin | Liste des admins |
| POST | `/api/admins` | Admin | Créer un admin |
| PUT | `/api/admins/:id` | Admin | Modifier un admin |
| DELETE | `/api/admins/:id` | Admin | Supprimer un admin |

---

## Authentification

Toutes les routes **Admin** nécessitent un header :

```
Authorization: Bearer <token>
```

Le token est obtenu via `POST /api/auth/login`.

**Exemple de login :**

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mirokai.fr", "password": "admin123"}'
```

Réponse :

```json
{
  "token": "eyJ...",
  "admin": { "id": "...", "email": "admin@mirokai.fr", "display_name": "Administrateur" }
}
```

---

## Upload de fichiers

```bash
curl -X POST http://localhost:5000/api/upload?folder=images \
  -H "Authorization: Bearer <token>" \
  -F "file=@/chemin/vers/image.jpg"
```

Réponse :

```json
{
  "url": "/uploads/images/uuid.jpg",
  "filename": "uuid.jpg"
}
```

Types autorisés : `png`, `jpg`, `jpeg`, `gif`, `webp`, `mp4`, `webm`, `mp3`, `wav`, `ogg`, `m4a`
Taille max : 100 Mo (configurable via `MAX_CONTENT_LENGTH`)

---

## Tranches d'âge (quiz)

Les valeurs valides pour `age_group` sont :

```
5-7 | 8-10 | 11-13 | 14+
```

---

## Dépendances

```
flask               # Framework web
flask-cors          # Cross-Origin Resource Sharing
flask-jwt-extended  # Authentification JWT
bcrypt              # Hachage des mots de passe
python-dotenv       # Chargement du fichier .env
```
