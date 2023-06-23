import sqlite3

def create_database():
    conn = sqlite3.connect('geotest.db')

def create_table():
    conn = sqlite3.connect('geotest.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    hash TEXT NOT NULL
                    )''')
    conn.commit()