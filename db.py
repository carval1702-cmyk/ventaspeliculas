import sqlite3

DB_NAME = "ventas_peliculas.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS peliculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def agregar_pelicula(titulo, genero, precio):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO peliculas (titulo, genero, precio) VALUES (?, ?, ?)", 
                   (titulo, genero, precio))
    conn.commit()
    conn.close()

def obtener_peliculas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM peliculas")
    peliculas = cursor.fetchall()
    conn.close()
    return peliculas
