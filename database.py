import sqlite3

DATABASE_NAME = "starwars.db"


def get_db_connection():
    """Membuka koneksi ke database dengan row factory untuk akses kolom berdasarkan nama."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Membuat tabel jika belum ada."""
    conn = get_db_connection()
    c = conn.cursor()

    # Tabel planets
    c.execute("""
        CREATE TABLE IF NOT EXISTS planets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            climate TEXT,
            terrain TEXT
        )
    """)

    # Tabel characters
    c.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            species TEXT,
            home_planet_id INTEGER,
            faction_id INTEGER,
            FOREIGN KEY (home_planet_id) REFERENCES planets (id),
            FOREIGN KEY (faction_id) REFERENCES factions (id)
        )
    """)

    # Tabel starships
    c.execute("""
        CREATE TABLE IF NOT EXISTS starships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            model TEXT,
            manufacturer TEXT
        )
    """)

    # Tabel penghubung characters-starships (many-to-many)
    c.execute("""
        CREATE TABLE IF NOT EXISTS character_starships (
            character_id INTEGER,
            starship_id INTEGER,
            PRIMARY KEY (character_id, starship_id),
            FOREIGN KEY (character_id) REFERENCES characters (id),
            FOREIGN KEY (starship_id) REFERENCES starships (id)
        )
    """)

    # Tabel factions
    c.execute("""
        CREATE TABLE IF NOT EXISTS factions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Tabel missions
    c.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    """)

    # Commit and close
    conn.commit()
    conn.close()
    print("Tabel berhasil dibuat.")


def get_max_value(table: str, column: str):
    """Mengembalikan nilai maksimum dari kolom tertentu di tabel yang diberikan."""
    conn = get_db_connection()
    c = conn.cursor()
    query = f"SELECT MAX({column}) AS max_value FROM {table}"  # Pastikan table dan column terverifikasi
    c.execute(query)
    row = c.fetchone()
    conn.close()
    return row["max_value"] if row else None


if __name__ == "__main__":
    init_db()
