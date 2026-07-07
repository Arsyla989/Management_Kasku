# KasKu - Aplikasi Manajemen Kas Kelas

KasKu adalah aplikasi desktop berbasis Python dengan arsitektur Model-View-Controller (MVC) yang digunakan untuk mengelola keuangan kas kelas secara digital, transparan, dan efisien.

## Fitur Utama

- **Autentikasi Admin**: Login aman untuk wali kelas atau bendahara kelas.
- **Manajemen Siswa**: Menambah, mengedit, dan menghapus data siswa.
- **Pembayaran Kas**: Pencatatan iuran kas masuk secara harian/mingguan.
- **Pengeluaran Kas**: Pencatatan dana keluar beserta keterangannya.
- **Laporan Keuangan**: Tampilan sisa kas, total masuk, total keluar.
- **Ekspor Data**: Mendukung ekspor laporan ke format Excel dan PDF.
- **Visualisasi Data**: Grafik tren kas masuk dan keluar menggunakan Chart.

## Struktur Project

```text
KasKu/
│
├── main.py
│
├── config/
│   └── settings.py
│
├── database/
│   ├── database.py
│   ├── init_db.py
│   └── kas_kelas.db (Dihasilkan otomatis)
│
├── models/
│   ├── admin.py
│   ├── siswa.py
│   ├── pembayaran.py
│   └── pengeluaran.py
│
├── controllers/
│   ├── auth_controller.py
│   ├── siswa_controller.py
│   ├── pembayaran_controller.py
│   ├── pengeluaran_controller.py
│   └── laporan_controller.py
│
├── views/
│   ├── login_view.py
│   ├── dashboard_view.py
│   ├── siswa_view.py
│   ├── pembayaran_view.py
│   ├── pengeluaran_view.py
│   └── laporan_view.py
│
├── services/
│   ├── excel_service.py
│   ├── report_service.py
│   └── chart_service.py
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── logo.png
│
├── exports/
│   ├── excel/
│   └── pdf/
│
├── utils/
│   ├── helpers.py
│   ├── validator.py
│   └── constants.py
│
├── requirements.txt
└── README.md
```

## Persyaratan Sistem

- Python 3.8 atau lebih baru
- Ketergantungan pustaka di `requirements.txt`

## Cara Instalasi & Menjalankan

1. Clone atau salin folder project ini.
2. Buka terminal di direktori project `KasKu/`.
3. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Inisialisasi database:
   ```bash
   python database/init_db.py
   ```
5. Jalankan aplikasi:
   ```bash
   python main.py
   ```

## Lisensi
MIT License
