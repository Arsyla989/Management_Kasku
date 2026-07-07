from typing import List, Optional
from database.database import execute_query

class Pengeluaran:
    def __init__(self, id: Optional[int] = None, keterangan: str = "", nominal: int = 0, tanggal: str = "") -> None:
        self.id = id
        self.keterangan = keterangan
        self.nominal = nominal
        self.tanggal = tanggal

    @classmethod
    def get_all(cls) -> List['Pengeluaran']:
        query = "SELECT id, keterangan, nominal, tanggal FROM pengeluaran ORDER BY tanggal DESC, id DESC"
        rows = execute_query(query)
        return [cls(id=r['id'], keterangan=r['keterangan'], nominal=r['nominal'], tanggal=r['tanggal']) for r in rows]

    @classmethod
    def get_by_id(cls, pengeluaran_id: int) -> Optional['Pengeluaran']:
        query = "SELECT id, keterangan, nominal, tanggal FROM pengeluaran WHERE id = ?"
        rows = execute_query(query, (pengeluaran_id,))
        if rows:
            r = rows[0]
            return cls(id=r['id'], keterangan=r['keterangan'], nominal=r['nominal'], tanggal=r['tanggal'])
        return None

    @classmethod
    def get_total_pengeluaran(cls) -> int:
        query = "SELECT SUM(nominal) FROM pengeluaran"
        rows = execute_query(query)
        return rows[0][0] if rows and rows[0][0] is not None else 0

    @classmethod
    def search(cls, keyword: str) -> List['Pengeluaran']:
        query = "SELECT id, keterangan, nominal, tanggal FROM pengeluaran WHERE keterangan LIKE ? ORDER BY tanggal DESC, id DESC"
        rows = execute_query(query, (f"%{keyword}%",))
        return [cls(id=r['id'], keterangan=r['keterangan'], nominal=r['nominal'], tanggal=r['tanggal']) for r in rows]

    def save(self) -> 'Pengeluaran':
        if self.id is None:
            query = "INSERT INTO pengeluaran (keterangan, nominal, tanggal) VALUES (?, ?, ?)"
            self.id = execute_query(query, (self.keterangan, self.nominal, self.tanggal), commit=True)
        else:
            query = "UPDATE pengeluaran SET keterangan = ?, nominal = ?, tanggal = ? WHERE id = ?"
            execute_query(query, (self.keterangan, self.nominal, self.tanggal, self.id), commit=True)
        return self

    @classmethod
    def delete(cls, pengeluaran_id: int) -> bool:
        query = "DELETE FROM pengeluaran WHERE id = ?"
        execute_query(query, (pengeluaran_id,), commit=True)
        return True
