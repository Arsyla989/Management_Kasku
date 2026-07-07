from typing import Dict, Any, List, Tuple, Optional
import os
from datetime import datetime
from models.siswa import Siswa
from models.pembayaran import Pembayaran
from models.pengeluaran import Pengeluaran
from models.activity_log import ActivityLog
from services.excel_service import ExcelService
from services.chart_service import ChartService
from services.report_service import ReportService  # PDF Export
from config import settings

class LaporanController:
    INDONESIAN_MONTHS = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }

    def __init__(self, app_context) -> None:
        self.app_context = app_context

    def get_current_indonesian_month(self) -> str:
        month_idx = datetime.now().month
        return self.INDONESIAN_MONTHS.get(month_idx, "Januari")

    def get_ringkasan_dashboard(self, bulan: str = "") -> Dict[str, Any]:
        """
        Mengambil semua angka statistik yang dibutuhkan oleh dashboard utama.
        """
        if not bulan:
            bulan = self.get_current_indonesian_month()
            
        total_siswa = len(Siswa.get_all())
        total_masuk = Pembayaran.get_total_pemasukan()
        total_keluar = Pengeluaran.get_total_pengeluaran()
        saldo = total_masuk - total_keluar
        rata_rata_saldo = saldo // 12 if saldo > 0 else 0
        
        # Hitung lunas / belum lunas untuk bulan terpilih
        lunas_count, belum_lunas_count = Pembayaran.get_lunas_summary_by_bulan(bulan)
        
        return {
            "total_siswa": total_siswa,
            "total_pemasukan": total_masuk,
            "total_pengeluaran": total_keluar,
            "saldo_kas": saldo,

            "rata_rata_saldo": rata_rata_saldo,

            "siswa_lunas": lunas_count,
            "siswa_belum_lunas": belum_lunas_count,
            "bulan_aktif": bulan
        }

    def generate_chart(self) -> Optional[str]:
        """
        Membuat grafik bulanan pemasukan vs pengeluaran dan menyimpan gambarnya.
        """
        try:
            # Kumpulkan data pembayaran per bulan
            pembayaran_list = Pembayaran.get_all()
            pengeluaran_list = Pengeluaran.get_all()
            
            # Hitung data bulanan
            data_bulanan: Dict[str, Dict[str, int]] = {}
            for b in self.INDONESIAN_MONTHS.values():
                data_bulanan[b] = {"masuk": 0, "keluar": 0}
                
            for p in pembayaran_list:
                if p.bulan in data_bulanan:
                    data_bulanan[p.bulan]["masuk"] += p.nominal
                    
            for exp in pengeluaran_list:
                # Dapatkan bulan dari tanggal pengeluaran (format: YYYY-MM-DD HH:MM:SS)
                try:
                    dt = datetime.strptime(exp.tanggal, "%Y-%m-%d %H:%M:%S")
                    m_idx = dt.month
                    m_name = self.INDONESIAN_MONTHS.get(m_idx, "")
                    if m_name in data_bulanan:
                        data_bulanan[m_name]["keluar"] += exp.nominal
                except Exception:
                    pass
            
            # Hasilkan grafik batang menggunakan service
            chart_path = ChartService.generate_monthly_chart(data_bulanan)
            return chart_path
        except Exception as e:
            print(f"[Chart Error]: Gagal menghasilkan grafik: {e}")
            return None

    def get_data_bulanan(self):

        pembayaran_list = Pembayaran.get_all()
        pengeluaran_list = Pengeluaran.get_all()

        data_bulanan = {}

        saldo_berjalan = 0

        for bulan in self.INDONESIAN_MONTHS.values():

            masuk = sum(
                p.nominal
                for p in pembayaran_list
                if p.bulan == bulan
            )
            keluar = 0
            for exp in pengeluaran_list:
                try:
                    dt = datetime.strptime(
                        exp.tanggal,
                        "%Y-%m-%d %H:%M:%S"
                    )

                    if self.INDONESIAN_MONTHS[dt.month] == bulan:
                        keluar += exp.nominal
                except:
                    pass
            saldo_awal = saldo_berjalan
            saldo_akhir = saldo_awal + masuk - keluar
            data_bulanan[bulan] = {
                "masuk": masuk,
                "keluar": keluar,
                "saldo_awal": saldo_awal,
                "saldo_akhir": saldo_akhir
            }

            saldo_berjalan = saldo_akhir

        return data_bulanan

    def ekspor_excel(self) -> Tuple[bool, str]:
        """
        Mengekspor semua data ke format spreadsheet Excel menggunakan OpenPyXL.
        """
        try:
            siswa_list = Siswa.get_all()
            pembayaran_list = Pembayaran.get_all()
            pengeluaran_list = Pengeluaran.get_all()
            
            bulan_terpilih = self.get_current_indonesian_month()
            status_pembayaran = Pembayaran.get_status_pembayaran_by_bulan(bulan_terpilih)
            
            filepath = ExcelService.export_all_data(
                siswa_list, 
                pembayaran_list, 
                pengeluaran_list, 
                status_pembayaran,
                bulan_terpilih
            )
            
            # Catat log
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(username, "Ekspor Excel", f"Mengekspor laporan keuangan kelas ke Excel: {os.path.basename(filepath)}")
            
            return True, f"Data berhasil diekspor ke:\n{filepath}"
        except Exception as e:
            import traceback
            return False, f"Gagal mengekspor data: {str(e)}\n\n{traceback.format_exc()}"

    def ekspor_pdf(self) -> Tuple[bool, str]:
        """
        Mengekspor laporan keuangan ringkas ke format PDF.
        """
        try:
            pembayaran_list = Pembayaran.get_all()
            pengeluaran_list = Pengeluaran.get_all()
            
            bulan_aktif = self.get_current_indonesian_month()
            ringkasan = self.get_ringkasan_dashboard(bulan_aktif)
            
            filepath = ReportService.export_laporan_pdf(pembayaran_list, pengeluaran_list, ringkasan)
            
            # Catat log
            username = self.app_context.current_user.username if self.app_context.current_user else "system"
            ActivityLog.record(username, "Ekspor PDF", f"Mengekspor laporan keuangan kelas ke PDF: {os.path.basename(filepath)}")
            
            return True, f"Laporan PDF berhasil diekspor ke:\n{filepath}"
        except Exception as e:
            import traceback
            return False, f"Gagal ekspor PDF: {str(e)}\n\n{traceback.format_exc()}"

    def get_audit_logs(self) -> List[ActivityLog]:
        return ActivityLog.get_all()
