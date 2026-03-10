import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
DATABASE_PATH = os.getenv("DATABASE_PATH", "./mirokai.db")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 104857600))  # 100MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "mp4", "webm", "mp3", "wav", "ogg", "m4a"}
