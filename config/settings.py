import os
import sys

# Base directory of the project
if getattr(sys, 'frozen', False):
    # Running as a bundled executable, BASE_DIR is where the executable is
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running in development environment
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database Configuration
DB_PATH = os.path.join(BASE_DIR, 'database', 'kas_kelas.db')

# Application Settings
APP_NAME = "KasKu"
APP_VERSION = "1.1.0"
WINDOW_SIZE = "1600x900"

# Target Kas bulanan per siswa
KAS_BULANAN_NOMINAL = 8000

# Export & Backup Directories
EXPORTS_DIR = os.path.join(BASE_DIR, 'exports')
EXCEL_EXPORT_DIR = os.path.join(EXPORTS_DIR, 'excel')
PDF_EXPORT_DIR = os.path.join(EXPORTS_DIR, 'pdf')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

# Theme Colors (Indonesian banking style)
COLOR_WHITE = "#FFFFFF"

COLOR_PRIMARY = "#6366F1"
COLOR_SECONDARY = "#0F172A"
COLOR_BACKGROUND = "#F8FAFC"

COLOR_SUCCESS = "#22C55E"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"

COLOR_TEXT_PRIMARY = "#111827"
COLOR_TEXT_MUTED = "#6B7280"

# Ensure directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(EXCEL_EXPORT_DIR, exist_ok=True)
os.makedirs(PDF_EXPORT_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

