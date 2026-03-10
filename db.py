import sqlite3
import os
import uuid
from config import DATABASE_PATH

def get_db():
    db_path = os.path.abspath(DATABASE_PATH)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with get_db() as conn:
        with open(schema_path, "r") as f:
            conn.executescript(f.read())
    print("Database initialized.")

def generate_id():
    return str(uuid.uuid4())

if __name__ == "__main__":
    init_db()
