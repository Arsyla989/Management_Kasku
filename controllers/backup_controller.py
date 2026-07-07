import os
import shutil
from datetime import datetime
from typing import Tuple, List
from config import settings
from models.activity_log import ActivityLog

class BackupController:
    def __init__(self, app_context) -> None:
        self.app_context = app_context

    def backup_database(self) -> Tuple[bool, str]:
        """
        Melakukan salinan file database SQLite saat ini ke folder backups/.
        """
        if not os.path.exists(settings.DB_PATH):
            return False, "File database asal tidak ditemukan!"
            
        try:
            os.makedirs(settings.BACKUP_DIR, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"kas_kelas_backup_{timestamp}.db"
            backup_path = os.path.join(settings.BACKUP_DIR, backup_filename)
            
            # Lakukan copy file
            shutil.copy2(settings.DB_PATH, backup_path)
            
            # Catat log
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(username, "Backup Database", f"Membuat cadangan database: {backup_filename}")
            
            return True, f"Database berhasil dicadangkan ke:\n{backup_path}"
        except Exception as e:
            return False, f"Gagal mencadangkan database: {str(e)}"

    def get_backup_list(self) -> List[str]:
        """
        Mengembalikan daftar file cadangan database yang ada di folder backups/.
        """
        if not os.path.exists(settings.BACKUP_DIR):
            return []
        files = [f for f in os.listdir(settings.BACKUP_DIR) if f.startswith("kas_kelas_backup_") and f.endswith(".db")]
        return sorted(files, reverse=True)
