import hashlib
from typing import Optional
from database.database import execute_query

class Admin:
    def __init__(self, id: int, username: str) -> None:
        self.id = id
        self.username = username

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional['Admin']:
        """
        Memverifikasi kredensial login admin menggunakan SHA256.
        """
        hashed = cls.hash_password(password)
        query = "SELECT id, username FROM admin WHERE username = ? AND password = ?"
        rows = execute_query(query, (username, hashed))
        
        if rows:
            row = rows[0]
            return cls(id=row['id'], username=row['username'])
        return None

    @classmethod
    def update_password(cls, admin_id: int, new_password: str) -> bool:
        """
        Mengubah password admin.
        """
        hashed = cls.hash_password(new_password)
        query = "UPDATE admin SET password = ? WHERE id = ?"
        execute_query(query, (hashed, admin_id), commit=True)
        return True
