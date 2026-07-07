from typing import Tuple
from models.admin import Admin
from models.activity_log import ActivityLog

class AuthController:
    def __init__(self, app_context) -> None:
        self.app_context = app_context

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Mengautentikasi pengguna admin dan memperbarui state utama aplikasi.
        """
        if not username or not password:
            return False, "Username dan password wajib diisi!"
            
        admin = Admin.authenticate(username, password)
        if admin:
            self.app_context.current_user = admin
            # Catat aktivitas login
            ActivityLog.record(admin.username, "Login", "Admin berhasil masuk ke sistem.")
            self.app_context.show_dashboard()
            return True, "Login berhasil!"
        else:
            return False, "Username atau password salah!"

    def logout(self) -> Tuple[bool, str]:
        """
        Mendestruksi sesi admin saat ini.
        """
        if self.app_context.current_user:
            ActivityLog.record(self.app_context.current_user.username, "Logout", "Admin keluar dari sistem.")
        self.app_context.current_user = None
        self.app_context.show_login()
        return True, "Logout berhasil!"
