from typing import List, Tuple
from models.siswa import Siswa
from models.activity_log import ActivityLog

class SiswaController:
    def __init__(self, app_context) -> None:
        self.app_context = app_context

    def get_all_siswa(self) -> List[Siswa]:
        return Siswa.get_all()

    def search_siswa(self, keyword: str) -> List[Siswa]:
        if not keyword.strip():
            return Siswa.get_all()
        return Siswa.search(keyword)

    def tambah_siswa(self, nis: str, nama: str, kelas: str) -> Tuple[bool, str]:
        """
        Menambahkan data siswa baru.
        """
        if not nis.strip() or not nama.strip() or not kelas.strip():
            return False, "Semua input field wajib diisi!"
            
        if not nis.isdigit():
            return False, "NIS harus berupa angka!"
            
        try:
            # Periksa duplikasi NIS
            all_siswa = Siswa.get_all()
            if any(s.nis == nis for s in all_siswa):
                return False, "NIS sudah terdaftar!"
                
            siswa = Siswa(nis=nis, nama=nama, kelas=kelas)
            siswa.save()
            
            # Catat aktivitas
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(username, "Tambah Siswa", f"Menambahkan siswa baru: {nama} ({nis}) - {kelas}")
            
            return True, "Data siswa berhasil ditambahkan!"
        except Exception as e:
            return False, f"Gagal menambahkan data: {str(e)}"

    def edit_siswa(self, siswa_id: int, nis: str, nama: str, kelas: str) -> Tuple[bool, str]:
        """
        Memperbarui data siswa yang ada.
        """
        if not nis.strip() or not nama.strip() or not kelas.strip():
            return False, "Semua input field wajib diisi!"
            
        if not nis.isdigit():
            return False, "NIS harus berupa angka!"
            
        try:
            # Periksa duplikasi NIS (abaikan data sendiri)
            all_siswa = Siswa.get_all()
            if any(s.nis == nis and s.id != siswa_id for s in all_siswa):
                return False, "NIS sudah digunakan oleh siswa lain!"
                
            siswa = Siswa(id=siswa_id, nis=nis, nama=nama, kelas=kelas)
            siswa.save()
            
            # Catat aktivitas
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(username, "Edit Siswa", f"Memperbarui data siswa ID {siswa_id}: {nama} ({nis})")
            
            return True, "Data siswa berhasil diperbarui!"
        except Exception as e:
            return False, f"Gagal memperbarui data: {str(e)}"

    def hapus_siswa(self, siswa_id: int) -> Tuple[bool, str]:
        """
        Menghapus data siswa berdasarkan ID.
        """
        try:
            siswa = Siswa.get_by_id(siswa_id)
            if not siswa:
                return False, "Siswa tidak ditemukan!"
                
            Siswa.delete(siswa_id)
            
            # Catat aktivitas
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(username, "Hapus Siswa", f"Menghapus siswa: {siswa.nama} ({siswa.nis})")
            
            return True, "Data siswa berhasil dihapus!"
        except Exception as e:
            return False, f"Gagal menghapus data: {str(e)}"
