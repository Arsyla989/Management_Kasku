from typing import List, Dict, Any, Optional, Tuple
from database.database import execute_query
from config import settings

class Pembayaran:
    def __init__(self, id: Optional[int] = None, siswa_id: int = 0, bulan: str = "", nominal: int = 0, tanggal: str = "", nama_siswa: str = "", kelas_siswa: str = "") -> None:
        self.id = id
        self.siswa_id = siswa_id
        self.bulan = bulan
        self.nominal = nominal
        self.tanggal = tanggal
        self.nama_siswa = nama_siswa
        self.kelas_siswa = kelas_siswa

    @classmethod
    def get_all(cls) -> List['Pembayaran']:
        query = """
        SELECT p.id, p.siswa_id, p.bulan, p.nominal, p.tanggal, s.nama as nama_siswa, s.kelas as kelas_siswa
        FROM pembayaran p
        JOIN siswa s ON p.siswa_id = s.id
        ORDER BY p.tanggal DESC, p.id DESC
        """
        rows = execute_query(query)
        return [cls(
            id=r['id'],
            siswa_id=r['siswa_id'],
            bulan=r['bulan'],
            nominal=r['nominal'],
            tanggal=r['tanggal'],
            nama_siswa=r['nama_siswa'],
            kelas_siswa=r['kelas_siswa']
        ) for r in rows]

    @classmethod
    def get_by_id(cls, pembayaran_id: int) -> Optional['Pembayaran']:
        query = """
        SELECT p.id, p.siswa_id, p.bulan, p.nominal, p.tanggal, s.nama as nama_siswa, s.kelas as kelas_siswa
        FROM pembayaran p
        JOIN siswa s ON p.siswa_id = s.id
        WHERE p.id = ?
        """
        rows = execute_query(query, (pembayaran_id,))
        if rows:
            r = rows[0]
            return cls(
                id=r['id'],
                siswa_id=r['siswa_id'],
                bulan=r['bulan'],
                nominal=r['nominal'],
                tanggal=r['tanggal'],
                nama_siswa=r['nama_siswa'],
                kelas_siswa=r['kelas_siswa']
            )
        return None

    @classmethod
    def search_and_filter(cls, keyword: str = "", bulan: str = "") -> List['Pembayaran']:
        """
        Mencari dan memfilter riwayat pembayaran berdasarkan keyword nama siswa dan/atau filter bulan.
        """
        query = """
        SELECT p.id, p.siswa_id, p.bulan, p.nominal, p.tanggal, s.nama as nama_siswa, s.kelas as kelas_siswa
        FROM pembayaran p
        JOIN siswa s ON p.siswa_id = s.id
        WHERE 1=1
        """
        params: List[Any] = []
        if keyword:
            query += " AND (s.nama LIKE ? OR s.nis LIKE ? OR s.kelas LIKE ?)"
            like_kw = f"%{keyword}%"
            params.extend([like_kw, like_kw, like_kw])
        if bulan and bulan != "Semua Bulan":
            query += " AND p.bulan = ?"
            params.append(bulan)
            
        query += " ORDER BY p.tanggal DESC, p.id DESC"
        rows = execute_query(query, tuple(params))
        return [cls(
            id=r['id'],
            siswa_id=r['siswa_id'],
            bulan=r['bulan'],
            nominal=r['nominal'],
            tanggal=r['tanggal'],
            nama_siswa=r['nama_siswa'],
            kelas_siswa=r['kelas_siswa']
        ) for r in rows]

    @classmethod
    def get_total_pemasukan(cls) -> int:
        query = "SELECT SUM(nominal) FROM pembayaran"
        rows = execute_query(query)
        return rows[0][0] if rows and rows[0][0] is not None else 0

    @classmethod
    def get_status_pembayaran_by_bulan(cls, bulan: str) -> List[Dict[str, Any]]:
        """
        Mendapatkan status pembayaran Lunas/Belum Lunas setiap siswa untuk bulan tertentu.
        Status dinyatakan Lunas jika total pembayaran siswa pada bulan tersebut >= KAS_BULANAN_NOMINAL.
        """
        query_siswa = "SELECT id, nis, nama, kelas FROM siswa ORDER BY nama ASC"
        siswa_rows = execute_query(query_siswa)
        
        query_bayar = "SELECT siswa_id, SUM(nominal) as total_bayar FROM pembayaran WHERE bulan = ? GROUP BY siswa_id"
        bayar_rows = execute_query(query_bayar, (bulan,))
        
        bayar_dict = {row['siswa_id']: row['total_bayar'] for row in bayar_rows}
        
        status_list = []
        target = settings.KAS_BULANAN_NOMINAL
        
        for s in siswa_rows:
            total_bayar = bayar_dict.get(s['id'], 0)
            status = "Lunas" if total_bayar >= target else "Belum Lunas"
            status_list.append({
                "id": s['id'],
                "nis": s['nis'],
                "nama": s['nama'],
                "kelas": s['kelas'],
                "total_bayar": total_bayar,
                "status": status
            })
            
        return status_list

    @classmethod
    def get_lunas_summary_by_bulan(cls, bulan: str) -> Tuple[int, int]:
        """
        Mengembalikan jumlah siswa (Lunas, Belum Lunas) untuk bulan tertentu.
        """
        statuses = cls.get_status_pembayaran_by_bulan(bulan)
        lunas = sum(1 for s in statuses if s['status'] == "Lunas")
        belum_lunas = len(statuses) - lunas
        return lunas, belum_lunas

    def save(self) -> 'Pembayaran':
        if self.id is None:
            query = "INSERT INTO pembayaran (siswa_id, bulan, nominal, tanggal) VALUES (?, ?, ?, ?)"
            self.id = execute_query(query, (self.siswa_id, self.bulan, self.nominal, self.tanggal), commit=True)
        else:
            query = "UPDATE pembayaran SET siswa_id = ?, bulan = ?, nominal = ?, tanggal = ? WHERE id = ?"
            execute_query(query, (self.siswa_id, self.bulan, self.nominal, self.tanggal, self.id), commit=True)
        return self

    @classmethod
    def delete(cls, pembayaran_id: int) -> bool:
        query = "DELETE FROM pembayaran WHERE id = ?"
        execute_query(query, (pembayaran_id,), commit=True)
        return True
