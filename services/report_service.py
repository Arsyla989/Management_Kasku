import os
from fpdf import FPDF
from datetime import datetime
from config import settings
from typing import List, Dict, Any

class PDFReport(FPDF):
    def header(self) -> None:
        # Title Bar (Blue Primary Fill)
        self.set_fill_color(15, 98, 254) # #0F62FE Primary
        self.rect(0, 0, 210, 25, 'F')
        
        self.set_y(5)
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'LAPORAN KEUANGAN KAS KELAS (KASKU)', border=False, align='C', new_x="LMARGIN", new_y="NEXT")
        
        self.set_y(28)
        self.ln(5)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(127, 140, 141)
        self.cell(0, 10, f'Halaman {self.page_no()}/{{nb}} - Dihasilkan otomatis oleh KasKu', align='C')

class ReportService:
    @staticmethod
    def export_laporan_pdf(
        pembayaran_list: List[Any],
        pengeluaran_list: List[Any],
        ringkasan: Dict[str, Any]
    ) -> str:
        pdf = PDFReport()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # 1. Summary Cards Section
        pdf.set_y(35)
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(30, 58, 138) # #1E3A8A Secondary
        pdf.cell(0, 8, 'I. RINGKASAN SALDO KEUANGAN', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        pdf.set_font('helvetica', '', 10)
        pdf.set_text_color(31, 41, 55) # Text Dark
        
        # Draw stats table
        pdf.set_fill_color(245, 247, 250) # Light BG
        
        pdf.cell(60, 8, '  Total Siswa Terdaftar', border=1, fill=True)
        pdf.cell(100, 8, f'  {ringkasan["total_siswa"]} Siswa', border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.cell(60, 8, '  Total Pemasukan Kas', border=1, fill=True)
        pdf.cell(100, 8, f'  Rp {ringkasan["total_pemasukan"]:,.0f}'.replace(",", "."), border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.cell(60, 8, '  Total Pengeluaran Kas', border=1, fill=True)
        pdf.cell(100, 8, f'  Rp {ringkasan["total_pengeluaran"]:,.0f}'.replace(",", "."), border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(60, 8, '  Saldo Kas Saat Ini', border=1, fill=True)
        pdf.cell(100, 8, f'  Rp {ringkasan["saldo_kas"]:,.0f}'.replace(",", "."), border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(10)
        
        # 2. Pembayaran Kas Masuk Section
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 8, 'II. RIWAYAT TRANSAKSI KAS MASUK (TERBARU)', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        # Table Headers
        pdf.set_font('helvetica', 'B', 9)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(15, 98, 254) # Primary Blue
        
        pdf.cell(10, 7, 'No', border=1, align='C', fill=True)
        pdf.cell(65, 7, 'Nama Siswa', border=1, align='C', fill=True)
        pdf.cell(30, 7, 'Bulan Iuran', border=1, align='C', fill=True)
        pdf.cell(35, 7, 'Nominal (Rp)', border=1, align='C', fill=True)
        pdf.cell(45, 7, 'Tanggal Bayar', border=1, align='C', fill=True, new_x="LMARGIN", new_y="NEXT")
        
        # Table Rows
        pdf.set_font('helvetica', '', 9)
        pdf.set_text_color(31, 41, 55)
        for idx, p in enumerate(pembayaran_list[:15], 1):
            pdf.cell(10, 6, str(idx), border=1, align='C')
            nama = p.nama_siswa[:25] + '..' if len(p.nama_siswa) > 25 else p.nama_siswa
            pdf.cell(65, 6, f' {nama}', border=1)
            pdf.cell(30, 6, p.bulan, border=1, align='C')
            pdf.cell(35, 6, f'{p.nominal:,.0f}'.replace(",", "."), border=1, align='R')
            
            tgl = p.tanggal.split(" ")[0] if " " in p.tanggal else p.tanggal
            pdf.cell(45, 6, tgl, border=1, align='C', new_x="LMARGIN", new_y="NEXT")
            
        if len(pembayaran_list) > 15:
            pdf.set_font('helvetica', 'I', 8)
            pdf.cell(0, 6, f'* Menampilkan 15 dari {len(pembayaran_list)} transaksi kas masuk terbaru.', new_x="LMARGIN", new_y="NEXT")
            
        pdf.ln(10)
        
        # 3. Pengeluaran Kas Keluar Section
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 8, 'III. RIWAYAT PENGELUARAN KAS (TERBARU)', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        # Table Headers
        pdf.set_font('helvetica', 'B', 9)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(30, 58, 138) # Secondary Dark Blue
        
        pdf.cell(10, 7, 'No', border=1, align='C', fill=True)
        pdf.cell(90, 7, 'Keterangan Pengeluaran', border=1, align='C', fill=True)
        pdf.cell(40, 7, 'Nominal (Rp)', border=1, align='C', fill=True)
        pdf.cell(45, 7, 'Tanggal Pengeluaran', border=1, align='C', fill=True, new_x="LMARGIN", new_y="NEXT")
        
        # Table Rows
        pdf.set_font('helvetica', '', 9)
        pdf.set_text_color(31, 41, 55)
        for idx, exp in enumerate(pengeluaran_list[:15], 1):
            pdf.cell(10, 6, str(idx), border=1, align='C')
            ket = exp.keterangan[:38] + '..' if len(exp.keterangan) > 38 else exp.keterangan
            pdf.cell(90, 6, f' {ket}', border=1)
            pdf.cell(40, 6, f'{exp.nominal:,.0f}'.replace(",", "."), border=1, align='R')
            
            tgl = exp.tanggal.split(" ")[0] if " " in exp.tanggal else exp.tanggal
            pdf.cell(45, 6, tgl, border=1, align='C', new_x="LMARGIN", new_y="NEXT")
            
        if len(pengeluaran_list) > 15:
            pdf.set_font('helvetica', 'I', 8)
            pdf.cell(0, 6, f'* Menampilkan 15 dari {len(pengeluaran_list)} transaksi pengeluaran terbaru.', new_x="LMARGIN", new_y="NEXT")
            
        # Save File
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Laporan_KasKu_{timestamp}.pdf"
        filepath = os.path.join(settings.PDF_EXPORT_DIR, filename)
        pdf.output(filepath)
        
        return filepath
