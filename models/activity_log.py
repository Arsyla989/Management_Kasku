from typing import List, Optional
from datetime import datetime
from database.database import execute_query

class ActivityLog:
    def __init__(self, id: Optional[int] = None, tanggal: str = "", username: str = "", aktivitas: str = "", detail: str = "") -> None:
        self.id = id
        self.tanggal = tanggal
        self.username = username
        self.aktivitas = aktivitas
        self.detail = detail

    @classmethod
    def record(cls, username: str, aktivitas: str, detail: str) -> 'ActivityLog':
        """
        Mencatat aktivitas log audit baru ke database.
        """
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO activity_log (tanggal, username, aktivitas, detail) VALUES (?, ?, ?, ?)"
        log_id = execute_query(query, (tanggal, username, aktivitas, detail), commit=True)
        return cls(id=log_id, tanggal=tanggal, username=username, aktivitas=aktivitas, detail=detail)

    @classmethod
    def get_all(cls) -> List['ActivityLog']:
        """
        Mengambil semua data audit log terbaru.
        """
        query = "SELECT id, tanggal, username, aktivitas, detail FROM activity_log ORDER BY tanggal DESC LIMIT 100"
        rows = execute_query(query)
        return [cls(
            id=r['id'],
            tanggal=r['tanggal'],
            username=r['username'],
            aktivitas=r['aktivitas'],
            detail=r['detail']
        ) for r in rows]
