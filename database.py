import sqlite3

def create_database():
    # Create database or create it if it does not exist
    conn = sqlite3.connect('geotest.db')

def create_table():
    # Connect
    conn = sqlite3.connect('geotest.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    hash TEXT NOT NULL
                    )''')
    
    conn.commit()