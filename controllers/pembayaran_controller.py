from typing import List, Tuple, Dict, Any
from datetime import datetime
from models.pembayaran import Pembayaran
from models.siswa import Siswa
from models.activity_log import ActivityLog

class PembayaranController:
    def __init__(self, app_context) -> None:
        self.app_context = app_context

    def get_all_pembayaran(self) -> List[Pembayaran]:
        return Pembayaran.get_all()

    def search_and_filter_pembayaran(self, keyword: str, bulan: str) -> List[Pembayaran]:
        return Pembayaran.search_and_filter(keyword, bulan)

    def get_status_pembayaran_by_bulan(self, bulan: str) -> List[Dict[str, Any]]:
        return Pembayaran.get_status_pembayaran_by_bulan(bulan)

    def catat_pembayaran(self, siswa_id: int, bulan: str, nominal_str: str) -> Tuple[bool, str]:
        """
        Mencatat pembayaran uang kas baru.
        """
        if not siswa_id or not bulan or not nominal_str.strip():
            return False, "Semua input wajib diisi!"
            
        if bulan == "Pilih Bulan":
            return False, "Silakan pilih bulan iuran kas!"
            
        try:
            nominal = int(nominal_str)
            if nominal <= 0:
                return False, "Nominal pembayaran harus lebih besar dari 0!"
        except ValueError:
            return False, "Nominal pembayaran harus berupa angka!"

        try:
            siswa = Siswa.get_by_id(siswa_id)
            if not siswa:
                return False, "Siswa tidak ditemukan!"
                
            tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pembayaran = Pembayaran(
                siswa_id=siswa_id,
                bulan=bulan,
                nominal=nominal,
                tanggal=tanggal
            )
            pembayaran.save()
            
            # Catat aktivitas
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(
                username, 
                "Pencatatan Kas Masuk", 
                f"Mencatat iuran {siswa.nama} untuk bulan {bulan} sebesar Rp {nominal:,}"
            )
            
            return True, f"Pembayaran uang kas untuk {siswa.nama} berhasil dicatat!"
        except Exception as e:
            return False, f"Gagal mencatat pembayaran: {str(e)}"

    def hapus_pembayaran(self, pembayaran_id: int) -> Tuple[bool, str]:
        """
        Menghapus transaksi pembayaran kas.
        """
        try:
            pembayaran = Pembayaran.get_by_id(pembayaran_id)
            if not pembayaran:
                return False, "Transaksi tidak ditemukan!"
                
            Pembayaran.delete(pembayaran_id)
            
            # Catat aktivitas
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(
                username, 
                "Hapus Kas Masuk", 
                f"Menghapus pembayaran ID {pembayaran_id} ({pembayaran.nama_siswa} - {pembayaran.bulan} - Rp {pembayaran.nominal:,})"
            )
            
            return True, "Transaksi pembayaran kas berhasil dihapus!"
        except Exception as e:
            return False, f"Gagal menghapus transaksi: {str(e)}"
