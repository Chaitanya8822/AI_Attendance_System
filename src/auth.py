import sqlite3
import hashlib

# 🔐 Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_table():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    hashed_password = hash_password(password)

    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
              (username, hashed_password))

    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    hashed_password = hash_password(password)

    c.execute("SELECT * FROM users WHERE username=? AND password=?", 
              (username, hashed_password))

    data = c.fetchone()

    conn.close()
    return data
