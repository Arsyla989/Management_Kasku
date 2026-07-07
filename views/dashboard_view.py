import customtkinter as ctk
from PIL import Image
import os
from config import settings
from controllers.auth_controller import AuthController
from controllers.laporan_controller import LaporanController
from controllers.backup_controller import BackupController
from views.siswa_view import SiswaView
from views.pembayaran_view import PembayaranView
from views.pengeluaran_view import PengeluaranView
from views.laporan_view import LaporanView
from tkinter import messagebox, ttk

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, auth_controller, user) -> None:
        super().__init__(parent, fg_color=settings.COLOR_BACKGROUND)
        self.parent = parent
        self.auth_controller = auth_controller
        self.laporan_controller = LaporanController(self)
        self.backup_controller = BackupController(self)
        self.user = user
        
        self.current_content_frame = None
        self.buttons = {}
        
        # Simpan state untuk file gambar grafik agar tidak di-garbage collect
        self.chart_image = None
        
        self.init_ui()

    def init_ui(self) -> None:
        # 1. SIDEBAR NAVIGATION
        self.sidebar = ctk.CTkFrame(self, fg_color=settings.COLOR_SECONDARY, width=260, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo/Branding
        logo_lbl = ctk.CTkLabel(
            self.sidebar,
            text="💰 KasKu",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        )
        logo_lbl.pack(pady=30)
        
        # Navigation Items
        menu_items = [
            ("🏠 Dashboard", self.show_home),
            ("👨‍🎓 Data Siswa", self.show_siswa),
            ("💵 Kas Masuk", self.show_kas_masuk),
            ("📤 Kas Keluar", self.show_kas_keluar),
            ("📊 Laporan", self.show_laporan),
            ("💾 Backup", self.show_backup)
        ]
        for name, callback in menu_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {name}",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                fg_color="transparent",
                text_color="#E2E8F0",
                hover_color="#4F46E5",
                height=42,
                corner_radius=10,
                anchor="w",
                command=callback
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.buttons[name] = btn
            
        # Logout Button
        btn_logout = ctk.CTkButton(
            self.sidebar,
            text="  Logout",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            height=42,
            corner_radius=10,
            anchor="w",
            command=self.handle_logout
        )
        btn_logout.pack(side="bottom", fill="x", padx=15, pady=25)
        
        # 2. TOP HEADER
        self.header = ctk.CTkFrame(
            self,
            fg_color=settings.COLOR_WHITE,
            height=65,
            corner_radius=15,
            border_width=0,
            border_color="#E5E7EB"
        )
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        
        self.lbl_title = ctk.CTkLabel(
            self.header,
            text="📊 Ringkasan Keuangan Kelas",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        self.lbl_title.pack(side="left", padx=25, pady=18)
        
        self.lbl_user = ctk.CTkLabel(
    self.header,
    text=f"👋 Halo, {self.user.username.capitalize()}",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=12,
        weight="bold"
    ),
    text_color=settings.COLOR_TEXT_MUTED
)
        self.lbl_user.pack(side="right", padx=25, pady=20)
        
        # 3. CONTENT AREA
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Load home by default
        self.show_home() 

    def set_active_menu(self, name: str) -> None:
        for k, btn in self.buttons.items():
            if k == name:
                btn.configure(fg_color=settings.COLOR_PRIMARY, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color="#E2E8F0")

    def clear_content(self):

        if self.current_content_frame:

            self.current_content_frame.destroy()

            self.current_content_frame = None
    
    def show_home(self) -> None:
        self.clear_content()
        self.set_active_menu("Dashboard")
        self.lbl_title.configure(text="Dashboard Keuangan")
        
        # Create dashboard frame
        self.current_content_frame = ctk.CTkFrame(
            self.content_area,
            fg_color="transparent"
        )
        self.current_content_frame.pack(
            fill="both",
            expand=True
        )
        
        # Load data ringkasan
        stats = self.laporan_controller.get_ringkasan_dashboard()
        title_frame = ctk.CTkFrame(
            self.current_content_frame,
            fg_color="transparent"
        )
        title_frame.pack(fill="x", pady=(0,15))

        ctk.CTkLabel(
            title_frame,
            text="Dashboard Keuangan",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Ringkasan pemasukan, pengeluaran, dan saldo kas kelas",
            text_color=settings.COLOR_TEXT_MUTED
        ).pack(anchor="w")
        
        # Top Grid for Stats Cards (3 Columns x 2 Rows)
        card_grid = ctk.CTkFrame(self.current_content_frame, fg_color="transparent")
        card_grid.pack(fill="x", pady=(0, 20))
        
        # Helper to create stats card
        def create_card(parent, title, value, color_bg, color_border, color_text):
            card = ctk.CTkFrame(
                parent,
                fg_color=color_bg,
                border_width=0,
                height=130,
                corner_radius=18
            )
            card.pack_propagate(False)
            
            lbl_title = ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=11,
                    weight="bold"
                ),
                text_color=color_text
            )
            lbl_title.pack(anchor="w", padx=15, pady=(15, 2))
            
            lbl_val = ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=18,
                    weight="bold"
                ),
                text_color=color_text  
            )
            lbl_val.pack(anchor="w", padx=15, pady=(0, 10))
            return card
            

        # Card 1: Total Siswa
        c1 = create_card(
            card_grid,
            "👨‍🎓 TOTAL SISWA", 
            f"{stats['total_siswa']} Siswa", 
            "#EFF6FF", 
            "#BFDBFE", 
            settings.COLOR_PRIMARY
            )
        c1.pack(side="left", fill="x", expand=True, padx=(0,5))
        
        # Card 2: Total Pemasukan
        c2 = create_card(
            card_grid,
            "💰 TOTAL PEMASUKAN", 
            f"Rp {stats['total_pemasukan']:,}".replace(",", "."), 
            "#ECFDF5", "#A7F3D0", 
            settings.COLOR_SUCCESS)
        c2.pack(side="left", fill="x", expand=True, padx=5)
        
        # Card 3: Total Pengeluaran
        c3 = create_card(
            card_grid,
            "📤 TOTAL PENGELUARAN", 
            f"Rp {stats['total_pengeluaran']:,}".replace(",", "."), 
            "#FEF2F2", "#FECACA", 
            settings.COLOR_DANGER
            )
        c3.pack(side="left", fill="x", expand=True, padx=5)
        
        # Card 4: Saldo Kas
        c4 = create_card(
            card_grid,
            "🏦 SALDO KAS", 
            f"Rp {stats['saldo_kas']:,}".replace(",", "."), 
            "#EEF2F6", 
            "#CBD5E1", 
            settings.COLOR_SECONDARY)
        c4.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )
        c5 = create_card(
            card_grid,
            "📅 RATA-RATA",
            f"Rp {stats['rata_rata_saldo']:,}".replace(",", "."),
            "#F3E8FF",
            "#D8B4FE",
            "#9333EA"
        )
        c5.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5,0)
        )
        content_row = ctk.CTkFrame(
            self.current_content_frame,
            fg_color="transparent"
        )
        content_row.pack(
            fill="x",
            pady=(20,0)
        ) 

        graph_frame = ctk.CTkFrame(
            content_row,
            fg_color=settings.COLOR_WHITE,
            corner_radius=18
        )
        graph_frame.pack(
            side="left",
            fill="both",
            expand=True,
        )

        summary_frame = ctk.CTkFrame(
            content_row,
            fg_color=settings.COLOR_WHITE,
            width=340,
            corner_radius=18
        )
        summary_frame.pack(
            side="right",
            fill="y"
        )
        summary_frame.pack_propagate(False)
        ctk.CTkLabel(
            summary_frame,
            text="📋 Ringkasan",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=15)
        items = [
            ("💰 Total Kas Masuk", stats["total_pemasukan"], "#22C55E"),
            ("📤 Total Kas Keluar", stats["total_pengeluaran"], "#EF4444"),
            ("🏦 Saldo Akhir Tahun", stats["saldo_kas"], "#2563EB"),
            ("📅 Rata-rata Saldo", stats["rata_rata_saldo"], "#9333EA")
        ]

        for title, value, color in items:

            card = ctk.CTkFrame(
                summary_frame,
                fg_color="#FFFFFF",
                corner_radius=10,
                border_width=1,
                border_color="#E5E7EB"
            )

            card.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(
                card,
                text=title,
                text_color=color
            ).pack(anchor="w", padx=10, pady=(8,2))

            ctk.CTkLabel(
                card,
                text=f"Rp {value:,}".replace(",", "."),
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color
            ).pack(anchor="w", padx=10, pady=(0,8))

        lbl_graph_title = ctk.CTkLabel(
            graph_frame,
            text="📊 Grafik Keuangan Per Bulan",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=settings.COLOR_SECONDARY
        )
        lbl_graph_title.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.lbl_graph = ctk.CTkLabel( graph_frame, text="Sedang membuat grafik...")
        self.lbl_graph.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Trigger chart generation
        self.load_dashboard_chart()
        self.create_monthly_table()

    def create_monthly_table(self):
        table_frame = ctk.CTkFrame(
            self.current_content_frame,
            fg_color=settings.COLOR_WHITE,
            corner_radius=18
        )

        table_frame.pack(
            fill="x",
            pady=(20,0)
        )

        title = ctk.CTkLabel(
            table_frame,
            text="📋 Rincian Keuangan Per Bulan",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=15
        )
        tree = ttk.Treeview(
            table_frame,
            columns=(
                "no",
                "bulan",
                "masuk",
                "keluar",
                "saldo_awal",
                "saldo_akhir"
            ),
            show="headings",
            height=12
        )

        tree.heading("no", text="No")
        tree.heading("bulan", text="Bulan")
        tree.heading("masuk", text="Kas Masuk")
        tree.heading("keluar", text="Kas Keluar")
        tree.heading("saldo_awal", text="Saldo Awal")
        tree.heading("saldo_akhir", text="Saldo Akhir")

        tree.column("no", width=60, anchor="center")
        tree.column("bulan", width=150, anchor="center")
        tree.column("masuk", width=150, anchor="e")
        tree.column("keluar", width=150, anchor="e")
        tree.column("saldo_awal", width=150, anchor="e")
        tree.column("saldo_akhir", width=150, anchor="e")

        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )
        data = self.laporan_controller.get_data_bulanan()

        for i, (bulan, item) in enumerate(data.items(), start=1):
            tree.insert(
                "",
                "end",
                values=(
                    i,
                    bulan,
                    f"Rp {item['masuk']:,}".replace(",", "."),
                    f"Rp {item['keluar']:,}".replace(",", "."),
                    f"Rp {item['saldo_awal']:,}".replace(",", "."),
                    f"Rp {item['saldo_akhir']:,}".replace(",", ".")
                )
            )

    def load_dashboard_chart(self) -> None:
        chart_path = self.laporan_controller.generate_chart()
        if chart_path and os.path.exists(chart_path):
            try:
                # Muat grafik PNG menggunakan PIL dan konversi ke CTkImage agar tajam & responsif
                pil_img = Image.open(chart_path)
                self.chart_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(800,300))
                self.lbl_graph.configure(image=self.chart_image, text="")
            except Exception as e:
                self.lbl_graph.configure(text=f"Gagal memuat grafik: {e}")
        else:
            self.lbl_graph.configure(text="Tidak ada transaksi keuangan untuk membuat grafik.")

    def show_siswa(self) -> None:
        self.clear_content()
        self.set_active_menu("Data Siswa")
        self.lbl_title.configure(text="Manajemen Data Siswa")
        
        self.current_content_frame = SiswaView(self.content_area)
        self.current_content_frame.pack(fill="both", expand=True)

    def show_kas_masuk(self) -> None:
        self.clear_content()
        self.set_active_menu("Kas Masuk")
        self.lbl_title.configure(text="Pencatatan Kas Masuk (Pembayaran Siswa)")
        
        self.current_content_frame = PembayaranView(self.content_area)
        self.current_content_frame.pack(fill="both", expand=True)

    def show_kas_keluar(self) -> None:
        self.clear_content()
        self.set_active_menu("Kas Keluar")
        self.lbl_title.configure(text="Pencatatan Kas Keluar (Pengeluaran Kelas)")
        
        self.current_content_frame = PengeluaranView(self.content_area)
        self.current_content_frame.pack(fill="both", expand=True)

    def show_laporan(self) -> None:
        self.clear_content()
        self.set_active_menu("Laporan & Ekspor")
        self.lbl_title.configure(text="Laporan Keuangan & Ekspor Spreadsheet/PDF")
        
        self.current_content_frame = LaporanView(self.content_area)
        self.current_content_frame.pack(fill="both", expand=True)

    def show_backup(self) -> None:
        self.clear_content()
        self.set_active_menu("Backup Database")
        self.lbl_title.configure(text="Cadangkan & Pulihkan Database SQLite")
        
        # Simple Backup Frame
        self.current_content_frame = ctk.CTkFrame(self.content_area, fg_color=settings.COLOR_WHITE, border_width=1, border_color="#E5E7EB", corner_radius=8)
        self.current_content_frame.pack(fill="both", expand=True)
        
        lbl_head = ctk.CTkLabel(
            self.current_content_frame,
            text="Fitur Backup Database",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=settings.COLOR_SECONDARY
        )
        lbl_head.pack(
            anchor="w",
            padx=20,
            pady=(20,5)
        )
        
        lbl_desc = ctk.CTkLabel(
            self.current_content_frame,
            text="Gunakan fitur ini untuk membuat salinan file database Anda agar aman dari kehilangan data.",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=settings.COLOR_TEXT_MUTED
        )
        lbl_desc.pack(anchor="w", pady=(0, 20))
        
        btn_run_backup = ctk.CTkButton(
            self.current_content_frame,
            text="CADANGKAN SEKARANG (SQLITE BACKUP)",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=settings.COLOR_PRIMARY,
            text_color="white",
            height=40,
            command=self.run_db_backup
        )
        btn_run_backup.pack(anchor="w", pady=10)
        
        # Display list of existing backups
        lbl_list_title = ctk.CTkLabel(
            self.current_content_frame,
            text="Daftar Salinan Cadangan (Terbaru):",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_list_title.pack(anchor="w", pady=(25, 5))
        
        self.listbox_backup = ctk.CTkTextbox(self.current_content_frame, height=200, font=ctk.CTkFont(family="Segoe UI", size=11))
        self.listbox_backup.pack(fill="x", pady=5)
        
        self.refresh_backup_list()

    def refresh_backup_list(self) -> None:
        self.listbox_backup.configure(state="normal")
        self.listbox_backup.delete("1.0", "end")
        backups = self.backup_controller.get_backup_list()
        
        if not backups:
            self.listbox_backup.insert("1.0", "Belum ada file cadangan yang disimpan.")
        else:
            for idx, b in enumerate(backups, 1):
                self.listbox_backup.insert("end", f"{idx}. {b}\n")
        self.listbox_backup.configure(state="disabled")

    def run_db_backup(self) -> None:
        success, msg = self.backup_controller.backup_database()
        if success:
            messagebox.showinfo("Backup Sukses", msg)
            self.refresh_backup_list()
        else:
            messagebox.showerror("Backup Gagal", msg)

    def handle_logout(self) -> None:
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin logout?"):
            self.auth_controller.logout()
