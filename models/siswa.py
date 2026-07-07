from typing import List, Optional
from database.database import execute_query

class Siswa:
    def __init__(self, id: Optional[int] = None, nis: str = "", nama: str = "", kelas: str = "") -> None:
        self.id = id
        self.nis = nis
        self.nama = nama
        self.kelas = kelas

    @classmethod
    def get_all(cls) -> List['Siswa']:
        query = "SELECT id, nis, nama, kelas FROM siswa ORDER BY nama ASC"
        rows = execute_query(query)
        return [cls(id=r['id'], nis=r['nis'], nama=r['nama'], kelas=r['kelas']) for r in rows]

    @classmethod
    def get_by_id(cls, siswa_id: int) -> Optional['Siswa']:
        query = "SELECT id, nis, nama, kelas FROM siswa WHERE id = ?"
        rows = execute_query(query, (siswa_id,))
        if rows:
            r = rows[0]
            return cls(id=r['id'], nis=r['nis'], nama=r['nama'], kelas=r['kelas'])
        return None

    @classmethod
    def search(cls, keyword: str) -> List['Siswa']:
        """
        Mencari siswa berdasarkan nama, NIS, atau kelas.
        """
        query = "SELECT id, nis, nama, kelas FROM siswa WHERE nama LIKE ? OR nis LIKE ? OR kelas LIKE ? ORDER BY nama ASC"
        like_keyword = f"%{keyword}%"
        rows = execute_query(query, (like_keyword, like_keyword, like_keyword))
        return [cls(id=r['id'], nis=r['nis'], nama=r['nama'], kelas=r['kelas']) for r in rows]

    def save(self) -> 'Siswa':
        """
        Menyimpan data siswa baru ke database atau memperbarui yang ada.
        """
        if self.id is None:
            query = "INSERT INTO siswa (nis, nama, kelas) VALUES (?, ?, ?)"
            self.id = execute_query(query, (self.nis, self.nama, self.kelas), commit=True)
        else:
            query = "UPDATE siswa SET nis = ?, nama = ?, kelas = ? WHERE id = ?"
            execute_query(query, (self.nis, self.nama, self.kelas, self.id), commit=True)
        return self

    @classmethod
    def delete(cls, siswa_id: int) -> bool:
        query = "DELETE FROM siswa WHERE id = ?"
        execute_query(query, (siswa_id,), commit=True)
        return True
