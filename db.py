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
            precio REAL NOT NULL,
            poster TEXT
        )
    """)
    conn.commit()

    # Intentar agregar columna poster si no existe
    try:
        cursor.execute("ALTER TABLE peliculas ADD COLUMN poster TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # Ya existe, no pasa nada
        pass

    conn.close()


def agregar_pelicula(titulo, genero, precio, poster):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO peliculas (titulo, genero, precio, poster) VALUES (?, ?, ?, ?)",
        (titulo, genero, precio, poster)
    )
    conn.commit()
    conn.close()


def obtener_peliculas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, genero, precio, poster FROM peliculas")
    rows = cursor.fetchall()
    conn.close()
    return rows


def obtener_pelicula(id_):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, genero, precio, poster FROM peliculas WHERE id = ?", (id_,))
    row = cursor.fetchone()
    conn.close()
    return row


def actualizar_pelicula(id_, titulo, genero, precio, poster):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE peliculas
        SET titulo = ?, genero = ?, precio = ?, poster = ?
        WHERE id = ?
    """, (titulo, genero, precio, poster, id_))
    conn.commit()
    conn.close()


def eliminar_pelicula(id_):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM peliculas WHERE id = ?", (id_,))
    conn.commit()
    conn.close()
