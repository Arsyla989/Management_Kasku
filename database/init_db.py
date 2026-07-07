import sqlite3
import os
import sys
import hashlib
from datetime import datetime

# Tambahkan base directory ke python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_database() -> None:
    print(f"Menginisialisasi database baru di: {settings.DB_PATH}")
    
    # Hapus database lama jika ada untuk migrasi bersih
    if os.path.exists(settings.DB_PATH):
        try:
            os.remove(settings.DB_PATH)
            print("Database lama dihapus untuk migrasi ulang.")
        except Exception as e:
            print(f"Peringatan: Gagal menghapus database lama: {e}")
            
    # Buat direktori database jika belum ada
    os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabel Admin
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)
    
    # 2. Tabel Siswa
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nis TEXT UNIQUE NOT NULL,
        nama TEXT NOT NULL,
        kelas TEXT NOT NULL
    );
    """)
    
    # 3. Tabel Pembayaran (Kas Masuk)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pembayaran (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        siswa_id INTEGER NOT NULL,
        bulan TEXT NOT NULL,
        nominal INTEGER NOT NULL,
        tanggal TEXT NOT NULL,
        FOREIGN KEY (siswa_id) REFERENCES siswa (id) ON DELETE CASCADE
    );
    """)
    
    # 4. Tabel Pengeluaran (Kas Keluar)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pengeluaran (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keterangan TEXT NOT NULL,
        nominal INTEGER NOT NULL,
        tanggal TEXT NOT NULL
    );
    """)
    
    # 5. Tabel Activity Log (Audit)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanggal TEXT NOT NULL,
        username TEXT NOT NULL,
        aktivitas TEXT NOT NULL,
        detail TEXT NOT NULL
    );
    """)
    
    # Seed data Admin default
    cursor.execute("SELECT COUNT(*) FROM admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ("admin", hash_password("admin123"))
        )
        print("[SEED] Admin default dibuat: admin / admin123")
        
    # Seed data Siswa default
    cursor.execute("SELECT COUNT(*) FROM siswa")
    if cursor.fetchone()[0] == 0:
        siswa_data = [
            ("12001", "Ahmad Subarjo", "XII-RPL-1"),
            ("12002", "Budi Doremi", "XII-RPL-1"),
            ("12003", "Cynthia Bella", "XII-RPL-1"),
            ("12004", "Deni Saputra", "XII-RPL-2"),
            ("12005", "Elisa Anggraeni", "XII-RPL-2"),
            ("12006", "Farhan Gunawan", "XII-RPL-2")
        ]
        cursor.executemany("INSERT INTO siswa (nis, nama, kelas) VALUES (?, ?, ?)", siswa_data)
        print(f"[SEED] Berhasil menambahkan {len(siswa_data)} siswa.")
        
        # Seed Data Pembayaran untuk Siswa
        pembayaran_data = [
            (1, "Januari", 20000, "2026-01-10 09:30:00"),
            (1, "Februari", 20000, "2026-02-12 10:15:00"),
            (2, "Januari", 20000, "2026-01-11 11:20:00"),
            (3, "Januari", 20000, "2026-01-15 14:00:00"),
            (3, "Februari", 10000, "2026-02-18 15:45:00"), # Belum lunas (baru 10.000 dari target 20.000)
            (4, "Januari", 20000, "2026-01-12 08:30:00")
        ]
        cursor.executemany("INSERT INTO pembayaran (siswa_id, bulan, nominal, tanggal) VALUES (?, ?, ?, ?)", pembayaran_data)
        print(f"[SEED] Berhasil menambahkan {len(pembayaran_data)} transaksi pembayaran.")
        
        # Seed Data Pengeluaran
        pengeluaran_data = [
            ("Membeli Sapu dan Pengki Kelas", 35000, "2026-01-15 16:00:00"),
            ("Membeli Spidol dan Penghapus Papan Tulis", 15000, "2026-02-05 09:00:00")
        ]
        cursor.executemany("INSERT INTO pengeluaran (keterangan, nominal, tanggal) VALUES (?, ?, ?)", pengeluaran_data)
        print(f"[SEED] Berhasil menambahkan {len(pengeluaran_data)} transaksi pengeluaran.")
        
        # Seed Logs
        logs = [
            ("2026-01-10 09:30:00", "admin", "Pencatatan Kas Masuk", "Mencatat kas Ahmad Subarjo untuk bulan Januari sebesar Rp 20.000"),
            ("2026-01-15 16:00:00", "admin", "Pencatatan Kas Keluar", "Membeli Sapu dan Pengki Kelas sebesar Rp 35.000")
        ]
        cursor.executemany("INSERT INTO activity_log (tanggal, username, aktivitas, detail) VALUES (?, ?, ?, ?)", logs)

    conn.commit()
    conn.close()
    print("Database init selesai!")

if __name__ == "__main__":
    init_database()
