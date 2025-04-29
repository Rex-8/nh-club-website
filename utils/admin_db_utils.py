# admin_db_utils.py

import sqlite3
import hashlib
import os

DB_PATH = os.path.join('database', 'admin_site.db')

def init_admin_db():
    """Create the admin_users table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_admin_user(username: str, password: str):
    """Add a new admin user with a SHA-256 hashed password."""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT OR IGNORE INTO admin_users (username, password_hash) VALUES (?, ?)',
        (username, password_hash)
    )
    conn.commit()
    conn.close()

def populate_default_admins():
    """Initialize the DB and insert three default users."""
    init_admin_db()
    default_admins = [
        ('admin1', 'password1'),
        ('admin2', 'password2'),
        ('admin3', 'password3'),
    ]
    for username, pwd in default_admins:
        add_admin_user(username, pwd)
    print("Initialized admin_site.db with default admin users.")

if __name__ == '__main__':
    populate_default_admins()
