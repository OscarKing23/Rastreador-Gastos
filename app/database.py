import sqlite3
from flask import current_app

def get_db_connection(db_path=None):
    """Obtiene una conexión a la base de datos SQLite."""
    if db_path is None:
        db_path = current_app.config['DATABASE_PATH']
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=None):
    """Inicializa el esquema de la base de datos si no existe."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        date TEXT
    )
    ''')
    conn.commit()
    conn.close()
