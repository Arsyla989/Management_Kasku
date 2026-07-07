import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from controllers.siswa_controller import SiswaController
from config import settings

class SiswaView(ctk.CTkFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent, fg_color="transparent")
        # Inisialisasi controller (butuh main app context, didapat dari parent.master)
        # Parent adalah content_area, parent.master adalah DashboardView yang memiliki self.laporan_controller.app_context (yaitu main app)
        self.controller = SiswaController(parent.master.parent)
        self.selected_siswa_id = None
        
        self.init_ui()
        self.load_data()

    def init_ui(self) -> None:
        # Main split container (Left Form, Right Grid Table)
        # 1. FORM CONTAINER
        self.form_frame = ctk.CTkFrame(
            self,
            fg_color=settings.COLOR_WHITE,
            border_width=1,
            border_color="#E5E7EB",
            corner_radius=8,
            width=280
        )
        self.form_frame.pack(side="left", fill="y", padx=(0, 15))
        self.form_frame.pack_propagate(False)
        
        lbl_title = ctk.CTkLabel(
            self.form_frame,
            text="Formulir Data Siswa",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=settings.COLOR_SECONDARY
        )
        lbl_title.pack(anchor="w", padx=15, pady=(15, 15))
        
        # NIS Input
        lbl_nis = ctk.CTkLabel(
            self.form_frame,
            text="Nomor Induk Siswa (NIS)",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_nis.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.entry_nis = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Contoh: 12001",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            border_color="#D1D5DB"
        )
        self.entry_nis.pack(fill="x", padx=15, pady=(0, 10))
        
        # Nama Input
        lbl_nama = ctk.CTkLabel(
            self.form_frame,
            text="Nama Lengkap Siswa",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_nama.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.entry_nama = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Contoh: Ahmad Subarjo",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            border_color="#D1D5DB"
        )
        self.entry_nama.pack(fill="x", padx=15, pady=(0, 10))
        
        # Kelas Input
        lbl_kelas = ctk.CTkLabel(
            self.form_frame,
            text="Kelas",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_kelas.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.entry_kelas = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Contoh: XII-RPL-1",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            border_color="#D1D5DB"
        )
        self.entry_kelas.pack(fill="x", padx=15, pady=(0, 20))
        
        # Action Buttons
        self.btn_save = ctk.CTkButton(
            self.form_frame,
            text="SIMPAN DATA",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=settings.COLOR_PRIMARY,
            text_color="white",
            height=34,
            command=self.save_data
        )
        self.btn_save.pack(fill="x", padx=15, pady=5)
        
        self.btn_clear = ctk.CTkButton(
            self.form_frame,
            text="BATAL",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="#9CA3AF",
            hover_color="#6B7280",
            text_color="white",
            height=34,
            command=self.clear_form
        )
        self.btn_clear.pack(fill="x", padx=15, pady=5)
        
        self.btn_delete = ctk.CTkButton(
            self.form_frame,
            text="HAPUS SISWA",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=settings.COLOR_DANGER,
            hover_color="#DC2626",
            text_color="white",
            height=34,
            state="disabled",
            command=self.delete_data
        )
        self.btn_delete.pack(fill="x", padx=15, pady=5)

        # 2. TABLE GRID CONTAINER
        self.table_frame = ctk.CTkFrame(
            self,
            fg_color=settings.COLOR_WHITE,
            border_width=1,
            border_color="#E5E7EB",
            corner_radius=8
        )
        self.table_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        # Top Table Search Bar
        search_bar = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        search_bar.pack(fill="x", pady=(0, 10))
        
        self.entry_search = ctk.CTkEntry(
            search_bar,
            placeholder_text="Cari berdasarkan nama, NIS, atau kelas...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            border_color="#D1D5DB"
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_search = ctk.CTkButton(
            search_bar,
            text="CARI SISWA",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=settings.COLOR_SECONDARY,
            text_color="white",
            width=100,
            height=34,
            command=self.search_data
        )
        btn_search.pack(side="right")
        
        # Treeview Grid
        scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        # Setup modern Treeview style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"), background="#F3F4F6", foreground=settings.COLOR_TEXT_PRIMARY, borderwidth=1)
        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=35,
            fieldbackground="white"
        )
        style.map("Treeview", background=[("selected", settings.COLOR_PRIMARY)], foreground=[("selected", "white")])
        
        self.table = ttk.Treeview(
            self.table_frame,
            columns=("no", "id", "nis", "nama", "kelas"),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.table.yview)
        
        self.table.heading("no", text="No")
        self.table.heading("id", text="ID")
        self.table.heading("nis", text="NIS")
        self.table.heading("nama", text="Nama Siswa")
        self.table.heading("kelas", text="Kelas")
        
        self.table.column("no", width=40, anchor="center")
        self.table.column("id", width=0, stretch=False) # Hidden
        self.table.column("nis", width=90, anchor="center")
        self.table.column("nama", width=250, anchor="w")
        self.table.column("kelas", width=120, anchor="center")
        
        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.on_select_row)

    def load_data(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)
            
        siswa_list = self.controller.get_all_siswa()
        for idx, s in enumerate(siswa_list, 1):
            self.table.insert("", "end", values=(idx, s.id, s.nis, s.nama, s.kelas))

    def search_data(self) -> None:
        keyword = self.entry_search.get().strip()
        for row in self.table.get_children():
            self.table.delete(row)
            
        siswa_list = self.controller.search_siswa(keyword)
        for idx, s in enumerate(siswa_list, 1):
            self.table.insert("", "end", values=(idx, s.id, s.nis, s.nama, s.kelas))

    def on_select_row(self, event) -> None:
        selected = self.table.selection()
        if not selected:
            return
            
        row_data = self.table.item(selected[0], "values")
        self.selected_siswa_id = int(row_data[1])
        
        self.entry_nis.delete(0, tk.END)
        self.entry_nis.insert(0, row_data[2])
        
        self.entry_nama.delete(0, tk.END)
        self.entry_nama.insert(0, row_data[3])
        
        self.entry_kelas.delete(0, tk.END)
        self.entry_kelas.insert(0, row_data[4])
        
        self.btn_delete.configure(state="normal")
        self.btn_save.configure(text="PERBARUI DATA")

    def clear_form(self) -> None:
        self.selected_siswa_id = None
        self.entry_nis.delete(0, tk.END)
        self.entry_nama.delete(0, tk.END)
        self.entry_kelas.delete(0, tk.END)
        self.btn_delete.configure(state="disabled")
        self.btn_save.configure(text="SIMPAN DATA")
        self.table.selection_remove(self.table.selection())

    def save_data(self) -> None:
        nis = self.entry_nis.get().strip()
        nama = self.entry_nama.get().strip()
        kelas = self.entry_kelas.get().strip()
        
        if self.selected_siswa_id is None:
            # Create
            success, msg = self.controller.tambah_siswa(nis, nama, kelas)
        else:
            # Update
            success, msg = self.controller.edit_siswa(self.selected_siswa_id, nis, nama, kelas)
            
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Gagal", msg)

    def delete_data(self) -> None:
        if self.selected_siswa_id is None:
            return
            
        if messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus data siswa ini?\nSemua transaksi pembayaran iuran siswa ini akan ikut terhapus secara permanen!"):
            success, msg = self.controller.hapus_siswa(self.selected_siswa_id)
            if success:
                messagebox.showinfo("Sukses", msg)
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Gagal", msg)
