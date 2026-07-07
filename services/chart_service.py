import os
import numpy as np
import matplotlib
import matplotlib.ticker as ticker
matplotlib.use('Agg')  # Mencegah crash thread Tkinter
import matplotlib.pyplot as plt
from typing import Dict
from config import settings

class ChartService:
    @staticmethod
    def generate_monthly_chart(data_bulanan: Dict[str, Dict[str, int]]) -> str:
        """
        Menghasilkan chart perbandingan pemasukan vs pengeluaran bulanan.
        Mengembalikan path gambar PNG yang dihasilkan.
        """

        filtered = {
            k:v
            for k,v in data_bulanan.items()
            if (
                v["masuk"] > 0
                or v["keluar"] > 0
            )
        }

        months = list(filtered.keys())

        pemasukan = [
            filtered[m]["masuk"]
            for m in months
        ]

        pengeluaran = [
            filtered[m]["keluar"]
            for m in months
        ]

        pemasukan = [data_bulanan[m]["masuk"] for m in months]
        pengeluaran = [data_bulanan[m]["keluar"] for m in months]
        saldo = [pemasukan[i] - pengeluaran[i] for i in range(len(months))]

        x = np.arange(len(months))
        width = 0.22

        fig, ax = plt.subplots(
            figsize=(11, 5),
            facecolor="white"    
        )

        ax.bar(
            x - width,
            pemasukan,
            width,
            label="Kas Masuk",
            color="#3B82F6"
        )

        ax.bar(
            x,
            pengeluaran,
            width,
            label="Kas Keluar",
            color="#F87171"
        )

        ax.bar(
            x + width,
            saldo,
            width,
            label="Saldo",
            color="#10B981"
        )
        for bar in ax.patches:

            height = bar.get_height()

            if height != 0:

                ax.annotate(
                    f"{int(height/1000)}k",
                    (
                        bar.get_x() + bar.get_width()/2,
                        height
                    ),
                    ha="center",
                    va="bottom",
                    fontsize=8
                )
        ax.set_xticks(x)
        ax.set_xticklabels(
            months,
            rotation=25,
            ha="right"
        )

        ax.set_title(
            "Laporan Keuangan Bulanan",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_facecolor("#FFFFFF")

        fig.patch.set_facecolor("#FFFFFF")

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.3
        )
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(
                lambda x, pos:
                f"{int(x/1000)}k"
            )
        )
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.legend(
            loc="upper left",
            frameon=False
        )
        for bar in ax.patches:

            h = bar.get_height()

            if h != 0:

                ax.annotate(
                    f"{int(h/1000)}k",
                    (
                        bar.get_x() + bar.get_width()/2,
                        h
                    ),
                    ha="center",
                    fontsize=8
                )
        plt.tight_layout()

        chart_dir = settings.EXPORTS_DIR

        os.makedirs(chart_dir, exist_ok=True)

        chart_path = os.path.join(
            chart_dir,
            "temp_monthly_chart.png"
        )

        plt.savefig(
            chart_path,
            dpi=180,
            bbox_inches="tight"
        )

        plt.close()

        return chart_path
    
