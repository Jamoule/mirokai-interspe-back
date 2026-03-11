PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS admins (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    display_name TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    last_login_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS modules (
    id TEXT PRIMARY KEY,
    number INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    media_type TEXT,
    media_url TEXT,
    image_urls TEXT DEFAULT '[]',
    transcript_segments TEXT DEFAULT '[]',
    qr_code TEXT UNIQUE NOT NULL,
    position_x REAL DEFAULT 0.0,
    position_y REAL DEFAULT 0.0,
    has_quiz INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    suggested_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    module_id TEXT NOT NULL,
    age_group TEXT NOT NULL,
    question_text TEXT NOT NULL,
    secret_word TEXT,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS answers (
    id TEXT PRIMARY KEY,
    question_id TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct INTEGER NOT NULL DEFAULT 0,
    display_order INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS parcours_settings (
    id TEXT PRIMARY KEY,
    parcours_name TEXT NOT NULL DEFAULT 'Parcours Mirokai',
    plan_image_url TEXT,
    welcome_message TEXT,
    completion_message TEXT,
    completion_email_template TEXT,
    completion_redirect_url TEXT,
    estimated_duration_min INTEGER DEFAULT 30,
    is_active INTEGER NOT NULL DEFAULT 1,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
