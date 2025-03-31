import sqlite3

# Имя файла базы данных
DB_FILE = "barcode_database.db"

# Подключение к базе данных SQLite и создание таблицы, если она не существует
def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS barcodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT UNIQUE,
            recipient TEXT,
            address TEXT
        )
    """)
    conn.commit()
    return conn, cursor

# Функция для получения всех штрих-кодов из базы данных
def get_all_barcodes(cursor):
    cursor.execute("SELECT barcode, recipient, address FROM barcodes")
    return [{"barcode": row[0], "recipient": row[1], "address": row[2]} for row in cursor.fetchall()]

# Функция для добавления нового штрих-кода в базу данных
def add_barcode_to_db(cursor, conn, barcode: str, recipient: str, address: str):
    cursor.execute("INSERT OR IGNORE INTO barcodes (barcode, recipient, address) VALUES (?, ?, ?)",
                   (barcode, recipient, address))
    conn.commit()