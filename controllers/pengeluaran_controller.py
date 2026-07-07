from typing import List, Tuple
from datetime import datetime
from models.pengeluaran import Pengeluaran
from models.activity_log import ActivityLog

class PengeluaranController:
    def __init__(self, app_context) -> None:
        self.app_context = app_context

    def get_all_pengeluaran(self) -> List[Pengeluaran]:
        return Pengeluaran.get_all()

    def search_pengeluaran(self, keyword: str) -> List[Pengeluaran]:
        if not keyword.strip():
            return Pengeluaran.get_all()
        return Pengeluaran.search(keyword)

    def catat_pengeluaran(self, keterangan: str, nominal_str: str) -> Tuple[bool, str]:
        """
        Mencatat pengeluaran kas baru.
        """
        if not keterangan.strip() or not nominal_str.strip():
            return False, "Semua input wajib diisi!"
            
        try:
            nominal = int(nominal_str)
            if nominal <= 0:
                return False, "Nominal pengeluaran harus lebih besar dari 0!"
        except ValueError:
            return False, "Nominal pengeluaran harus berupa angka!"

        try:
            tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pengeluaran = Pengeluaran(
                keterangan=keterangan,
                nominal=nominal,
                tanggal=tanggal
            )
            pengeluaran.save()
            
            # Catat aktivitas
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(
                username,
                "Pencatatan Kas Keluar",
                f"Mencatat pengeluaran: {keterangan} sebesar Rp {nominal:,}"
            )
            
            return True, "Transaksi pengeluaran kas berhasil dicatat!"
        except Exception as e:
            return False, f"Gagal mencatat pengeluaran: {str(e)}"

    def edit_pengeluaran(self, pengeluaran_id: int, keterangan: str, nominal_str: str) -> Tuple[bool, str]:
        """
        Memperbarui data pengeluaran kas.
        """
        if not keterangan.strip() or not nominal_str.strip():
            return False, "Semua input wajib diisi!"
            
        try:
            nominal = int(nominal_str)
            if nominal <= 0:
                return False, "Nominal pengeluaran harus lebih besar dari 0!"
        except ValueError:
            return False, "Nominal pengeluaran harus berupa angka!"

        try:
            # Dapatkan tanggal lama agar tidak berubah
            old_p = Pengeluaran.get_by_id(pengeluaran_id)
            tanggal = old_p.tanggal if old_p else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            pengeluaran = Pengeluaran(
                id=pengeluaran_id,
                keterangan=keterangan,
                nominal=nominal,
                tanggal=tanggal
            )
            pengeluaran.save()
            
            # Catat aktivitas
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(
                username,
                "Edit Kas Keluar",
                f"Memperbarui pengeluaran ID {pengeluaran_id}: {keterangan} (Rp {nominal:,})"
            )
            
            return True, "Data pengeluaran kas berhasil diperbarui!"
        except Exception as e:
            return False, f"Gagal memperbarui pengeluaran: {str(e)}"

    def hapus_pengeluaran(self, pengeluaran_id: int) -> Tuple[bool, str]:
        """
        Menghapus transaksi pengeluaran.
        """
        try:
            pengeluaran = Pengeluaran.get_by_id(pengeluaran_id)
            if not pengeluaran:
                return False, "Transaksi pengeluaran tidak ditemukan!"
                
            Pengeluaran.delete(pengeluaran_id)
            
            # Catat aktivitas
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(
                username,
                "Hapus Kas Keluar",
                f"Menghapus pengeluaran ID {pengeluaran_id} ({pengeluaran.keterangan} - Rp {pengeluaran.nominal:,})"
            )
            
            return True, "Transaksi pengeluaran kas berhasil dihapus!"
        except Exception as e:
            return False, f"Gagal menghapus transaksi: {str(e)}"
