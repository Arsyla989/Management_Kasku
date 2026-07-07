import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from controllers.pengeluaran_controller import PengeluaranController
from config import settings

class PengeluaranView(ctk.CTkFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent, fg_color="transparent")
        self.controller = PengeluaranController(parent.master.parent)
        self.selected_pengeluaran_id = None
        
        self.init_ui()
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
            text="Form Pengeluaran Kas",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=settings.COLOR_SECONDARY
        )
        lbl_title.pack(anchor="w", padx=15, pady=(15, 15))
        
        # Keperluan/Keterangan
        lbl_ket = ctk.CTkLabel(
            self.form_frame,
            text="Keperluan / Keterangan",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_ket.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.entry_keterangan = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Contoh: Beli spidol kelas",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            border_color="#D1D5DB"
        )
        self.entry_keterangan.pack(fill="x", padx=15, pady=(0, 10))
        
        # Nominal
        lbl_nom = ctk.CTkLabel(
            self.form_frame,
            text="Nominal Pengeluaran (Rp)",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_PRIMARY
        )
        lbl_nom.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.entry_nominal = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Contoh: 15000",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            border_color="#D1D5DB"
        )
        self.entry_nominal.pack(fill="x", padx=15, pady=(0, 20))
        
        # Actions
        self.btn_save = ctk.CTkButton(
            self.form_frame,
            text="CATAT PENGELUARAN",
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
        
        # Search Frame
        search_bar = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        search_bar.pack(fill="x", pady=(0, 10))
        
        self.entry_search = ctk.CTkEntry(
            search_bar,
            placeholder_text="Cari berdasarkan keterangan pengeluaran...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color="#F9FAFB",
            border_color="#D1D5DB"
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_search = ctk.CTkButton(
            search_bar,
            text="CARI",
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
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#F3F4F6", foreground=settings.COLOR_TEXT_PRIMARY, borderwidth=1)
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=26, fieldbackground="white")
        style.map("Treeview", background=[("selected", settings.COLOR_PRIMARY)], foreground=[("selected", "white")])
        
        self.table = ttk.Treeview(
            self.table_frame,
            columns=("no", "id", "keterangan", "nominal", "tanggal"),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.table.yview)
        
        self.table.heading("no", text="No")
        self.table.heading("id", text="ID")
        self.table.heading("keterangan", text="Keterangan Pengeluaran")
        self.table.heading("nominal", text="Nominal (Rp)")
        self.table.heading("tanggal", text="Tanggal Transaksi")
        
        self.table.column("no", width=35, anchor="center")
        self.table.column("id", width=0, stretch=False)
        self.table.column("keterangan", width=250, anchor="w")
        self.table.column("nominal", width=100, anchor="e")
        self.table.column("tanggal", width=120, anchor="center")
        
        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.on_select_row)

    def load_data(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)
            
        exp_list = self.controller.get_all_pengeluaran()
        for idx, exp in enumerate(exp_list, 1):
            nom_str = f"{exp.nominal:,}".replace(",", ".")
            self.table.insert("", "end", values=(idx, exp.id, exp.keterangan, nom_str, exp.tanggal))

    def search_data(self) -> None:
        keyword = self.entry_search.get().strip()
        for row in self.table.get_children():
            self.table.delete(row)
            
        exp_list = self.controller.search_pengeluaran(keyword)
        for idx, exp in enumerate(exp_list, 1):
            nom_str = f"{exp.nominal:,}".replace(",", ".")
            self.table.insert("", "end", values=(idx, exp.id, exp.keterangan, nom_str, exp.tanggal))

    def on_select_row(self, event) -> None:
        selected = self.table.selection()
        if not selected:
            return
            
        row_data = self.table.item(selected[0], "values")
        self.selected_pengeluaran_id = int(row_data[1])
        
        self.entry_keterangan.delete(0, tk.END)
        self.entry_keterangan.insert(0, row_data[2])
        
        # Bersihkan titik ribuan nominal
        raw_nominal = row_data[3].replace(".", "")
        self.entry_nominal.delete(0, tk.END)
        self.entry_nominal.insert(0, raw_nominal)
        
        self.btn_delete.configure(state="normal")
        self.btn_save.configure(text="PERBARUI DATA")

    def clear_form(self) -> None:
        self.selected_pengeluaran_id = None
        self.entry_keterangan.delete(0, tk.END)
        self.entry_nominal.delete(0, tk.END)
        self.btn_delete.configure(state="disabled")
        self.btn_save.configure(text="CATAT PENGELUARAN")
        self.table.selection_remove(self.table.selection())

    def save_data(self) -> None:
        keterangan = self.entry_keterangan.get().strip()
        nominal = self.entry_nominal.get().strip()
        
        if self.selected_pengeluaran_id is None:
            # Create
            success, msg = self.controller.catat_pengeluaran(keterangan, nominal)
        else:
            # Update
            success, msg = self.controller.edit_pengeluaran(self.selected_pengeluaran_id, keterangan, nominal)
            
        if success:
            messagebox.showinfo("Sukses", msg)
            self.clear_form()
            self.load_data()
            # Trigger refresh stats di dashboard
            self.parent.master.show_home()
        else:
            messagebox.showerror("Gagal", msg)

    def delete_data(self) -> None:
        if self.selected_pengeluaran_id is None:
            return
            
        if messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus data pengeluaran ini?"):
            success, msg = self.controller.hapus_pengeluaran(self.selected_pengeluaran_id)
            if success:
                messagebox.showinfo("Sukses", msg)
                self.clear_form()
                self.load_data()
                # Trigger refresh stats di dashboard
                self.parent.master.show_home()
            else:
                messagebox.showerror("Gagal", msg)
