import sqlite3

def create_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            class_number TEXT,
            class_char TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_user_data(user_id, class_number, class_char):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        REPLACE INTO users (user_id, class_number, class_char)
        VALUES (?, ?, ?)
    ''', (user_id, class_number, class_char))
    conn.commit()
    conn.close()

def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        SELECT class_number, class_char
        FROM users
        WHERE user_id = ?
    ''', (user_id,))
    user_data = c.fetchone()
    conn.close()
    return user_data

def delete_user_data(user_id) : 
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        DELETE FROM users WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()
