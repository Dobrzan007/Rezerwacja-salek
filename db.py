# Reservation App: Python + Tkinter + SQLite
# File structure:
#   room_booking_app/
#     ├── main.py            # Entry point, GUI setup, login window
#     ├── db.py              # Database schema and helper functions
#     ├── models.py          # CRUD functions for rooms and reservations
#     ├── gui/
#     │    ├── login.py      # Login form for secretaries
#     │    ├── calendar_view.py  # Week-view calendar widget
#     │    ├── dialogs.py    # Add/Delete reservation dialogs
#     └── data/
#          └── booking.db    # SQLite database file

# Step 1: Initialize database and create tables

# db.py
import os
import sqlite3
import hashlib
import uuid

# Path configuration
db_dir = os.path.join(os.path.dirname(__file__), 'data')
DB_PATH = os.path.join(db_dir, 'booking.db')

# Ensure data directory exists and return a DB connection

def get_connection():
    os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize tables: admins (secretaries), rooms, reservations

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Admins table: only secretaries have accounts\    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT
        )
    ''')
    # Rooms table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    # Reservations table: anonymous users enter name/email and receive a token
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            user_name TEXT NOT NULL,
            user_email TEXT,
            token TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY(room_id) REFERENCES rooms(id)
        )
    ''')
    conn.commit()
    
    # Migration: add password_hash column if it doesn't exist
    try:
        cur.execute("ALTER TABLE reservations ADD COLUMN password_hash TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Migration: add email column to admins if it doesn't exist
    try:
        cur.execute("ALTER TABLE admins ADD COLUMN email TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    conn.close()

# Utility to hash admin passwords
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Utility to generate a unique token for each reservation
def generate_token() -> str:
    return uuid.uuid4().hex
