import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from controllers.laporan_controller import LaporanController
from config import settings

class LaporanView(ctk.CTkFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent, fg_color="transparent")
        self.controller = LaporanController(parent.master.parent)
        
        self.init_ui()
        self.refresh_data()

    def init_ui(self) -> None:
        # Two-panel layout
        # 1. LEFT PANEL (FINANCIAL SUMMARY & EXPORTS)
        left_panel = ctk.CTkFrame(
            self,
            fg_color=settings.COLOR_WHITE,
            border_width=1,
            border_color="#E5E7EB",
            corner_radius=8,
            width=320
        )
        left_panel.pack(side="left", fill="y", padx=(0, 15), pady=20)
        left_panel.pack_propagate(False)
        
        lbl_summary_title = ctk.CTkLabel(
            left_panel,
            text="Ringkasan Keuangan",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=settings.COLOR_SECONDARY
        )
        lbl_summary_title.pack(anchor="w", pady=(0, 15))
        
        # Pemasukan Card
        card_in = ctk.CTkFrame(left_panel, fg_color="#ECFDF5", border_width=1, border_color="#A7F3D0", height=65, corner_radius=6)
        card_in.pack(fill="x", pady=5)
        card_in.pack_propagate(False)
        tk.Label(card_in, text="Total Pemasukan", font=("Segoe UI", 8, "bold"), bg="#ECFDF5", fg=settings.COLOR_SUCCESS).pack(anchor="w", padx=15, pady=(8, 2))
        self.lbl_pemasukan = tk.Label(card_in, text="Rp 0", font=("Segoe UI", 12, "bold"), bg="#ECFDF5", fg=settings.COLOR_SUCCESS)
        self.lbl_pemasukan.pack(anchor="w", padx=15)
        
        # Pengeluaran Card
        card_out = ctk.CTkFrame(left_panel, fg_color="#FEF2F2", border_width=1, border_color="#FECACA", height=65, corner_radius=6)
        card_out.pack(fill="x", pady=5)
        card_out.pack_propagate(False)
        tk.Label(card_out, text="Total Pengeluaran", font=("Segoe UI", 8, "bold"), bg="#FEF2F2", fg=settings.COLOR_DANGER).pack(anchor="w", padx=15, pady=(8, 2))
        self.lbl_pengeluaran = tk.Label(card_out, text="Rp 0", font=("Segoe UI", 12, "bold"), bg="#FEF2F2", fg=settings.COLOR_DANGER)
        self.lbl_pengeluaran.pack(anchor="w", padx=15)
        
        # Saldo Card
        card_saldo = ctk.CTkFrame(left_panel, fg_color="#EFF6FF", border_width=1, border_color="#BFDBFE", height=65, corner_radius=6)
        card_saldo.pack(fill="x", pady=5)
        card_saldo.pack_propagate(False)
        tk.Label(card_saldo, text="Saldo Akhir Kas", font=("Segoe UI", 8, "bold"), bg="#EFF6FF", fg=settings.COLOR_PRIMARY).pack(anchor="w", padx=15, pady=(8, 2))
        self.lbl_saldo = tk.Label(card_saldo, text="Rp 0", font=("Segoe UI", 12, "bold"), bg="#EFF6FF", fg=settings.COLOR_PRIMARY)
        self.lbl_saldo.pack(anchor="w", padx=15)
        
        # Export Buttons
        lbl_export_title = ctk.CTkLabel(
            left_panel,
            text="Ekspor Data Laporan",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_export_title.pack(anchor="w", pady=(20, 10))
        
        btn_excel = ctk.CTkButton(
            left_panel,
            text="EKSPOR SPREADSHEET EXCEL",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=settings.COLOR_SUCCESS,
            hover_color="#059669",
            text_color="white",
            height=36,
            command=self.export_excel
        )
        btn_excel.pack(fill="x", pady=5)
        
        btn_pdf = ctk.CTkButton(
            left_panel,
            text="EKSPOR DOKUMEN PDF",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=settings.COLOR_PRIMARY,
            hover_color=settings.COLOR_SECONDARY,
            text_color="white",
            height=36,
            command=self.export_pdf
        )
        btn_pdf.pack(fill="x", pady=5)
        
        btn_refresh = ctk.CTkButton(
            left_panel,
            text="REFRESH DATA",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="#9CA3AF",
            hover_color="#6B7280",
            text_color="white",
            height=36,
            command=self.refresh_data
        )
        btn_refresh.pack(fill="x", pady=(20, 5))
        
        # 2. RIGHT PANEL (AUDIT ACTIVITY LOGS)
        right_panel = ctk.CTkFrame(
            self,
            fg_color=settings.COLOR_WHITE,
            border_width=1,
            border_color="#E5E7EB",
            corner_radius=8
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        lbl_logs_title = ctk.CTkLabel(
            right_panel,
            text="Log Audit Aktivitas Sistem",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=settings.COLOR_SECONDARY
        )
        lbl_logs_title.pack(anchor="w", pady=(0, 10))
        
        # Logs Grid
        scroll_y = ttk.Scrollbar(right_panel, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#F3F4F6", foreground=settings.COLOR_TEXT_PRIMARY, borderwidth=1)
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=26, fieldbackground="white")
        style.map("Treeview", background=[("selected", settings.COLOR_PRIMARY)], foreground=[("selected", "white")])
        
        self.table = ttk.Treeview(
            right_panel,
            columns=("no", "tanggal", "user", "aktivitas", "detail"),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.table.yview)
        
        self.table.heading("no", text="No")
        self.table.heading("tanggal", text="Tanggal Jam")
        self.table.heading("user", text="Admin")
        self.table.heading("aktivitas", text="Aktivitas")
        self.table.heading("detail", text="Detail Log")
        
        self.table.column("no", width=35, anchor="center")
        self.table.column("tanggal", width=120, anchor="center")
        self.table.column("user", width=70, anchor="center")
        self.table.column("aktivitas", width=120, anchor="w")
        self.table.column("detail", width=250, anchor="w")
        
        self.table.pack(fill="both", expand=True)

    def refresh_data(self) -> None:
        # Load stats
        stats = self.controller.get_ringkasan_dashboard()
        self.lbl_pemasukan.config(text=f"Rp {stats['total_pemasukan']:,}".replace(",", "."))
        self.lbl_pengeluaran.config(text=f"Rp {stats['total_pengeluaran']:,}".replace(",", "."))
        self.lbl_saldo.config(text=f"Rp {stats['saldo_kas']:,}".replace(",", "."))
        
        # Load audit logs
        for row in self.table.get_children():
            self.table.delete(row)
            
        logs = self.controller.get_audit_logs()
        for idx, l in enumerate(logs, 1):
            self.table.insert("", "end", values=(idx, l.tanggal, l.username, l.aktivitas, l.detail))

    def export_excel(self) -> None:
        success, msg = self.controller.ekspor_excel()
        if success:
            messagebox.showinfo("Sukses Ekspor", msg)
            self.refresh_data()
        else:
            messagebox.showerror("Gagal Ekspor", msg)

    def export_pdf(self) -> None:
        success, msg = self.controller.ekspor_pdf()
        if success:
            messagebox.showinfo("Sukses Ekspor", msg)
            self.refresh_data()
        else:
            messagebox.showerror("Gagal Ekspor", msg)
