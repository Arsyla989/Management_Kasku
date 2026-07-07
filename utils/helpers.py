import hashlib
from datetime import datetime

def format_rupiah(amount: int) -> str:
    """
    Memformat integer menjadi rupiah, contoh: Rp 20.000.
    """
    if amount is None:
        amount = 0
    return f"Rp {amount:,}".replace(",", ".")

def format_date(date_str: str) -> str:
    """
    Memformat tanggal database (YYYY-MM-DD HH:MM:SS) ke format Indonesia (DD-MM-YYYY).
    """
    if not date_str:
        return "-"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d-%m-%Y %H:%M")
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d-%m-%Y")
        except ValueError:
            return date_str
