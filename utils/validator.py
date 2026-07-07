import re

def validate_nis(nis):
    """
    Validasi NIS: Harus numerik dan biasanya antara 5 hingga 10 karakter.
    """
    if not nis:
        return False, "NIS tidak boleh kosong!"
    if not nis.isdigit():
        return False, "NIS harus berupa angka!"
    if not (5 <= len(nis) <= 10):
        return False, "NIS harus memiliki panjang 5 hingga 10 karakter!"
    return True, ""

def validate_nama(nama):
    """
    Validasi Nama: Tidak boleh kosong, hanya alfabet dan spasi.
    """
    if not nama:
        return False, "Nama tidak boleh kosong!"
    if len(nama.strip()) < 3:
        return False, "Nama minimal harus 3 karakter!"
    if not re.match(r"^[a-zA-Z\s'.]+$", nama):
        return False, "Nama hanya boleh mengandung huruf, spasi, kutip, atau titik!"
    return True, ""

def validate_number(value, field_name):
    """
    Validasi input angka (jumlah pembayaran/pengeluaran).
    """
    if not value:
        return False, f"{field_name} tidak boleh kosong!"
    try:
        val = float(value)
        if val <= 0:
            return False, f"{field_name} harus lebih besar dari 0!"
    except ValueError:
        return False, f"{field_name} harus diisi dengan angka valid!"
    return True, ""
