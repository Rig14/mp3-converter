CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password BLOB NOT NULL,
    name VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    motd TEXT DEFAULT 'Hello, World!',
    image TEXT DEFAULT 'default_user.svg'
);

CREATE TABLE HISTORY (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    content_title TEXT NOT NULL,
    content_url TEXT NOT NULL,
    content_format TEXT NOT NULL,
);