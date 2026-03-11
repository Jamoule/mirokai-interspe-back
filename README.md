# Mirokai API — Back-end

API back-end du parcours Mirokai, construite avec **Flask**, **SQLite** et **JWT**. Ce projet gère les modules, les quiz et l'administration du parcours.

---

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

| Outil | Version minimale | Vérification |
|---|---|---|
| **Python** | 3.10+ | `python3 --version` |
| **pip** | Inclus avec Python | `pip3 --version` |

*Note : SQLite est intégré à Python, aucune installation de base de données externe n'est requise.*

---

## Installation et Lancement

### 1. Se placer dans le dossier de l'API
```bash
cd api
```

### 2. Créer et activer l'environnement virtuel
```bash
# Création
python3 -m venv venv

# Activation (Linux / macOS)
source venv/bin/activate

# Activation (Windows)
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
Copiez le fichier d'exemple et éditez-le si nécessaire :
```bash
cp .env.example .env
```
*Le fichier `.env` contient les clés secrètes pour JWT et le chemin de la base de données.*

### 5. Initialiser la base de données
Cette étape crée les tables et un compte administrateur par défaut :
```bash
python seed.py
```
**Identifiants admin créés :**
- **Email** : `admin@mirokai.fr`
- **Mot de passe** : `admin123`

### 6. Lancer le serveur
```bash
# Mode développement avec auto-reload
flask run --port 5000 --debug
```
L'API sera accessible sur : `http://localhost:5000`

---

## Endpoints principaux

### Administration (Back-office)
Toutes les routes admin nécessitent le header : `Authorization: Bearer <token>`

- **Auth** : `POST /api/auth/login` (pour obtenir le token)
- **Modules** : `GET /api/modules/all`, `POST /api/modules`, `PATCH /api/modules/:id/position`
- **Questions** : `GET /api/modules/:id/questions/all`, `POST /api/questions`
- **Upload** : `POST /api/upload?folder=images` (images, vidéos, audio)
- **Settings** : `PUT /api/settings`

### Visiteurs
- **Modules** : `GET /api/modules` (liste active), `GET /api/modules/qr/:qr_code`
- **Quiz** : `GET /api/modules/:id/questions`, `POST /api/quiz/validate`

---

## Structure du projet
- `app.py` : Point d'entrée et configuration Flask.
- `routes/` : Blueprints par domaine (auth, modules, questions, etc.).
- `db.py` & `schema.sql` : Gestion de la base SQLite.
- `uploads/` : Stockage local des médias.
