import customtkinter as ctk
import os
import sys

# Tambahkan direktori root ke path pencarian modul Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from database.init_db import init_database
from controllers.auth_controller import AuthController
from views.login_view import LoginView
from views.dashboard_view import DashboardView

class KasKuApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        # Konfigurasi Tampilan Utama CustomTkinter
        ctk.set_appearance_mode("Light")  # Light mode untuk nuansa bersih perbankan
        ctk.set_default_color_theme("blue") # Blue color theme untuk mencocokkan Primary #0F62FE
        
        self.title(f"{settings.APP_NAME} - Sistem Manajemen Uang Kas Kelas")
        self.geometry(settings.WINDOW_SIZE)
        self.configure(fg_color=settings.COLOR_BACKGROUND)
        
        # State aplikasi
        self.current_user = None
        self.current_frame = None
        
        # Inisialisasi controller
        self.auth_controller = AuthController(self)
        
        # Inisialisasi database jika belum ada file DB
        if not os.path.exists(settings.DB_PATH):
            print("Database belum terdeteksi. Melakukan inisialisasi...")
            init_database()
            
        # Tampilkan halaman login pertama kali
        self.show_login()

    def show_frame(self, frame_class, *args, **kwargs) -> None:
        """
        Menghancurkan frame lama dan merender frame baru yang dipilih.
        """
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self) -> None:
        self.title(f"{settings.APP_NAME} - Login Admin")
        self.geometry("420x500") # Window pas untuk form login
        self.resizable(False, False)
        self.show_frame(LoginView, self.auth_controller)

    def show_dashboard(self) -> None:
        self.title(f"{settings.APP_NAME} - Dashboard Utama")
        self.geometry(settings.WINDOW_SIZE)
        self.resizable(True, True)
        self.show_frame(DashboardView, self.auth_controller, self.current_user)

if __name__ == "__main__":
    # DPI awareness untuk resolusi layar tinggi di Windows
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
            
    app = KasKuApp()
    app.mainloop()
