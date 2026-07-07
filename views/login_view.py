import customtkinter as ctk
from tkinter import messagebox
from config import settings

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, auth_controller) -> None:
        super().__init__(parent, fg_color=settings.COLOR_BACKGROUND)
        self.parent = parent
        self.controller = auth_controller
        self.init_ui()

    def init_ui(self) -> None:
        # Container Card
        card = ctk.CTkFrame(
            self,
            width=420,
            height=500, 
            fg_color=settings.COLOR_WHITE,
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Icon Placeholder
        logo_lbl = ctk.CTkLabel(
            card,
            text="💰 KasKu",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=settings.COLOR_PRIMARY
        )
        logo_lbl.pack(pady=(45, 5))
        
        subtitle_lbl = ctk.CTkLabel(
            card,
            text="Kelola Keuangan Kelas Secara Modern",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=settings.COLOR_TEXT_MUTED
        )
        subtitle_lbl.pack(pady=(0, 30))
        
        # Username Field
        username_lbl = ctk.CTkLabel(
            card,
            text="Username",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        username_lbl.pack(anchor="w", padx=45, pady=(5, 2))
        
        self.entry_username = ctk.CTkEntry(
            card,
            placeholder_text="Masukkan username admin",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=38,
            fg_color="#F9FAFB",
            border_color="#D1D5DB",
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        self.entry_username.pack(fill="x", padx=45, pady=(0, 15))
        self.entry_username.focus()

        # Password Field
        password_lbl = ctk.CTkLabel(
            card,
            text="Password",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        password_lbl.pack(anchor="w", padx=45, pady=(5, 2))
        
        self.entry_password = ctk.CTkEntry(
            card,
            placeholder_text="Masukkan password",
            show="*",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=38,
            fg_color="#F9FAFB",
            border_color="#D1D5DB",
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        self.entry_password.pack(fill="x", padx=45, pady=(0, 25))
        
        # Submit Button
        self.btn_login = ctk.CTkButton(
            card,
            text="MASUK KE SISTEM",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=settings.COLOR_PRIMARY,
            hover_color=settings.COLOR_SECONDARY,
            text_color="white",
            height=48,
            corner_radius=12,
            command=self.handle_login
        )
        self.btn_login.pack(fill="x", padx=45, pady=(0, 20))
        
        # Footer branding
        footer_lbl = ctk.CTkLabel(
            card,
            text="v1.1.0 © DeepMind Antigravity",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color="#9CA3AF"
        )
        footer_lbl.pack(side="bottom", pady=15)
        
        # Enter key binding
        self.parent.bind("<Return>", lambda event: self.handle_login())

    def handle_login(self) -> None:
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        
        success, message = self.controller.login(username, password)
        if success:
            self.parent.unbind("<Return>")
        else:
            messagebox.showerror("Login Gagal", message)
