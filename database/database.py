import sqlite3
from typing import List, Dict, Any, Tuple, Optional
from config import settings

def get_connection() -> sqlite3.Connection:
    """
    Mendapatkan koneksi ke database SQLite dengan row_factory diaktifkan.
    """
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def execute_query(query: str, params: Tuple[Any, ...] = (), commit: bool = False) -> Any:
    """
    Menjalankan query SQL dengan parameter secara aman.
    Mengembalikan cursor.lastrowid jika commit=True, atau list of dict jika select.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return cursor.lastrowid
        else:
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[Database Error]: {e} | Query: {query} | Params: {params}")
        raise e
    finally:
        conn.close()
