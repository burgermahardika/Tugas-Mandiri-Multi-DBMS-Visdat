import sqlite3
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Mengambil path absolut berdasarkan letak file seed_data.py ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ecommerce_local.db")

# 1. Inisialisasi SQLite (DBMS 1: Data Produk)
def init_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unit_price REAL
        )
    """)
    
    products_data = [
        (1, 'Laptop Gaming Pro', 'Elektronik', 15000000),
        (2, 'Mechanical Keyboard', 'Elektronik', 750000),
        (3, 'Kursi Ergonomis', 'Furniture', 2500000),
        (4, 'Meja Standing Desk', 'Furniture', 4000000),
        (5, 'Mouse Wireless', 'Elektronik', 300000)
    ]
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products_data)
    conn.commit()
    conn.close()
    print(f"✅ SQLite (DBMS 1) berhasil diinisialisasi di: {DB_PATH}")

# 2. Inisialisasi PostgreSQL / Supabase (DBMS 2: Data Transaksi)
def init_postgres():
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        print("❌ URL PostgreSQL belum diset di file .env")
        return
        
    engine = create_engine(db_url)
    
    with engine.begin() as conn:
        conn.exec_driver_sql("DROP TABLE IF EXISTS transactions;")
        conn.exec_driver_sql("""
            CREATE TABLE transactions (
                transaction_id SERIAL PRIMARY KEY,
                product_id INT,
                quantity INT,
                transaction_date DATE,
                region TEXT
            );
        """)
        
        conn.exec_driver_sql("""
            INSERT INTO transactions (product_id, quantity, transaction_date, region) VALUES
            (1, 2, '2026-10-01', 'Jakarta'),
            (2, 5, '2026-10-02', 'Bandung'),
            (3, 1, '2026-10-03', 'Surabaya'),
            (4, 2, '2026-10-04', 'Jakarta'),
            (5, 10, '2026-10-05', 'Yogyakarta'),
            (1, 1, '2026-10-06', 'Bandung'),
            (2, 3, '2026-10-07', 'Surabaya');
        """)
    print("✅ PostgreSQL (DBMS 2) berhasil diinisialisasi!")

if __name__ == "__main__":
    init_sqlite()
    init_postgres()