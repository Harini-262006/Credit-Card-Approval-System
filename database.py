import sqlite3
import os

# Create database folder if it doesn't exist
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/credit.db")

cursor = conn.cursor()

# --------------------------
# Users Table
# --------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT
)
""")

# --------------------------
# Predictions Table
# --------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    income REAL,
    family REAL,
    children REAL,
    age REAL,
    employment REAL,
    result TEXT
)
""")

conn.commit()

conn.close()

print("Database Created Successfully")