import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from controllers.pembayaran_controller import PembayaranController
from controllers.siswa_controller import SiswaController
from config import settings

class PembayaranView(ctk.CTkFrame):
    MONTHS = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]

    def __init__(self, parent) -> None:
        super().__init__(parent, fg_color="transparent")
        self.controller = PembayaranController(parent.master.parent)
        self.siswa_controller = SiswaController(parent.master.parent)
        self.selected_pembayaran_id = None
        
        self.siswa_map = {}
        
        self.init_ui()
        self.load_siswa_combobox()
        self.load_data()

    def init_ui(self) -> None:
        # 1. LEFT FORM CONTAINER
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
            text="Catat Iuran Uang Kas",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=settings.COLOR_SECONDARY
        )
        lbl_title.pack(anchor="w", padx=15, pady=(15, 15))
        
        # Select Student
        lbl_siswa = ctk.CTkLabel(
            self.form_frame,
            text="Pilih Siswa",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_siswa.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.combo_siswa = ctk.CTkOptionMenu(
            self.form_frame,
            values=[],
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            button_color=settings.COLOR_PRIMARY,
            button_hover_color=settings.COLOR_SECONDARY,
            text_color=settings.COLOR_TEXT_PRIMARY,
            dropdown_text_color=settings.COLOR_TEXT_PRIMARY
        )
        self.combo_siswa.pack(fill="x", padx=15, pady=(0, 10))
        
        # Select Month
        lbl_month = ctk.CTkLabel(
            self.form_frame,
            text="Untuk Bulan Iuran",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_month.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.combo_bulan = ctk.CTkOptionMenu(
            self.form_frame,
            values=self.MONTHS,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            button_color=settings.COLOR_PRIMARY,
            button_hover_color=settings.COLOR_SECONDARY,
            text_color=settings.COLOR_TEXT_PRIMARY,
            dropdown_text_color=settings.COLOR_TEXT_PRIMARY
        )
        self.combo_bulan.pack(fill="x", padx=15, pady=(0, 10))
        
        # Nominal
        lbl_nom = ctk.CTkLabel(
            self.form_frame,
            text="Nominal (Rp)",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_nom.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.entry_nominal = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Contoh: 8000",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            border_color="#D1D5DB"
        )
        self.entry_nominal.pack(fill="x", padx=15, pady=(0, 20))
        self.entry_nominal.insert(0, str(settings.KAS_BULANAN_NOMINAL))
        
        # Actions
        self.btn_save = ctk.CTkButton(
            self.form_frame,
            text="CATAT PEMBAYARAN",
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
            text="HAPUS TRANSAKSI",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=settings.COLOR_DANGER,
            hover_color="#DC2626",
            text_color="white",
            height=34,
            state="disabled",
            command=self.delete_data
        )
        self.btn_delete.pack(fill="x", padx=15, pady=5)

        # 2. RIGHT GRID CONTAINER
        self.table_frame = ctk.CTkFrame(
            self,
            fg_color=settings.COLOR_WHITE,
            border_width=1,
            border_color="#E5E7EB",
            corner_radius=8
        )
        self.table_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        # Filters Header
        filter_bar = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        filter_bar.pack(fill="x", pady=(0, 10))
        
        self.entry_search = ctk.CTkEntry(
            filter_bar,
            placeholder_text="Cari berdasarkan nama siswa atau kelas...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            border_color="#D1D5DB"
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.combo_filter_bulan = ctk.CTkOptionMenu(
            filter_bar,
            values=["Semua Bulan"] + self.MONTHS,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            width=120,
            height=34,
            fg_color="#F9FAFB",
            button_color=settings.COLOR_SECONDARY,
            text_color=settings.COLOR_TEXT_PRIMARY,
            dropdown_text_color=settings.COLOR_TEXT_PRIMARY
        )
        self.combo_filter_bulan.pack(side="left", padx=(0, 10))
        self.combo_filter_bulan.set("Semua Bulan")
        
        btn_filter = ctk.CTkButton(
            filter_bar,
            text="FILTER & CARI",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=settings.COLOR_SECONDARY,
            text_color="white",
            width=100,
            height=34,
            command=self.search_and_filter_data
        )
        btn_filter.pack(side="right")
        
        # Treeview Grid
        scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
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
            columns=("no", "id", "nama", "kelas", "bulan", "nominal", "tanggal"),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.table.yview)
        
        self.table.heading("no", text="No")
        self.table.heading("id", text="ID")
        self.table.heading("nama", text="Nama Siswa")
        self.table.heading("kelas", text="Kelas")
        self.table.heading("bulan", text="Bulan Iuran")
        self.table.heading("nominal", text="Nominal (Rp)")
        self.table.heading("tanggal", text="Tanggal Bayar")
        
        self.table.column("no", width=35, anchor="center")
        self.table.column("id", width=0, stretch=False)
        self.table.column("nama", width=180, anchor="w")
        self.table.column("kelas", width=80, anchor="center")
        self.table.column("bulan", width=90, anchor="center")
        self.table.column("nominal", width=95, anchor="e")
        self.table.column("tanggal", width=120, anchor="center")
        
        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.on_select_row)

    def load_siswa_combobox(self) -> None:
        siswa_list = self.siswa_controller.get_all_siswa()
        self.siswa_map = {}
        names = []
        for s in siswa_list:
            display_name = f"{s.nama} ({s.nis})"
            self.siswa_map[display_name] = s.id
            names.append(display_name)
            
        if names:
            self.combo_siswa.configure(values=names)
            self.combo_siswa.set(names[0])
        else:
            self.combo_siswa.configure(values=["Belum ada data siswa"])
            self.combo_siswa.set("Belum ada data siswa")

    def load_data(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)
            
        pay_list = self.controller.get_all_pembayaran()
        for idx, p in enumerate(pay_list, 1):
            nom_str = f"{p.nominal:,}".replace(",", ".")
            self.table.insert("", "end", values=(idx, p.id, p.nama_siswa, p.kelas_siswa, p.bulan, nom_str, p.tanggal))

    def search_and_filter_data(self) -> None:
        keyword = self.entry_search.get().strip()
        bulan = self.combo_filter_bulan.get()
        
        for row in self.table.get_children():
            self.table.delete(row)
            
        pay_list = self.controller.search_and_filter_pembayaran(keyword, bulan)
        for idx, p in enumerate(pay_list, 1):
            nom_str = f"{p.nominal:,}".replace(",", ".")
            self.table.insert("", "end", values=(idx, p.id, p.nama_siswa, p.kelas_siswa, p.bulan, nom_str, p.tanggal))

    def on_select_row(self, event) -> None:
        selected = self.table.selection()
        if not selected:
            return
            
        row_data = self.table.item(selected[0], "values")
        self.selected_pembayaran_id = int(row_data[1])
        self.btn_delete.configure(state="normal")

    def clear_form(self) -> None:
        self.selected_pembayaran_id = None
        self.entry_nominal.delete(0, tk.END)
        self.entry_nominal.insert(0, str(settings.KAS_BULANAN_NOMINAL))
        self.btn_delete.configure(state="disabled")
        self.table.selection_remove(self.table.selection())

    def save_data(self) -> None:
        selected_display = self.combo_siswa.get()
        if selected_display == "Belum ada data siswa" or not selected_display:
            messagebox.showerror("Error", "Siswa tidak valid!")
            return
            
        siswa_id = self.siswa_map.get(selected_display)
        bulan = self.combo_bulan.get()
        nominal = self.entry_nominal.get().strip()
        
        success, msg = self.controller.catat_pembayaran(siswa_id, bulan, nominal)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_form()
            self.load_data()
            # Trigger refresh stats di dashboard
            self.parent.master.show_home()
        else:
            messagebox.showerror("Gagal", msg)

    def delete_data(self) -> None:
        if self.selected_pembayaran_id is None:
            return
            
        if messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus transaksi pembayaran uang kas ini?"):
            success, msg = self.controller.hapus_pembayaran(self.selected_pembayaran_id)
            if success:
                messagebox.showinfo("Sukses", msg)
                self.clear_form()
                self.load_data()
                # Trigger refresh stats di dashboard
                self.parent.master.show_home()
            else:
                messagebox.showerror("Gagal", msg)
