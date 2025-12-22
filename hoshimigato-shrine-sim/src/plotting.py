from __future__ import annotations
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def mode(series) -> str:
    if len(series) == 0:
        return ""
    return Counter(series).most_common(1)[0][0]

def plot_character_bundle(
    df: pd.DataFrame,
    out_pdf: str | Path,
    out_fig_dir: str | Path,
    band_half_width: int = 1,
    seed: int = 0
) -> dict:
    """
    Creates a multi-page PDF:
      - per character: (entropy + x1/x2/alpha) with event annotations, plus local zoom around entropy peak.
      - final page: peak-band summary.
    Saves per-character PNGs under out_fig_dir.
    """
    out_pdf = Path(out_pdf)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    out_fig_dir = Path(out_fig_dir)
    (out_fig_dir / "entropy_peak_zoom").mkdir(parents=True, exist_ok=True)

    meta = {}

    with PdfPages(out_pdf) as pdf:
        for ch, sub in df.groupby("character"):
            grp = sub.groupby('t').agg(
                x1_mean=('x1','mean'), x1_std=('x1','std'),
                x2_mean=('x2','mean'), x2_std=('x2','std'),
                alpha_mean=('alpha','mean'), alpha_std=('alpha','std'),
                ent_mean=('entropy','mean'), ent_std=('entropy','std'),
                event=('event_en', mode),
                n=('entropy','size')
            ).reset_index().sort_values('t')

            t_peak = float(grp.loc[grp['ent_mean'].idxmax(), 't'])
            t_min = float(max(grp['t'].min(), t_peak - band_half_width))
            t_max = float(min(grp['t'].max(), t_peak + band_half_width))

            # 4-panel plot
            fig, axes = plt.subplots(4,1, figsize=(10,10), sharex=True)
            axes[0].errorbar(grp['t'], grp['ent_mean'], yerr=grp['ent_std'].fillna(0), fmt='-o', capsize=3)
            axes[0].set_ylabel('Entropy')
            axes[0].axvline(t_peak, linestyle='--', linewidth=1)
            axes[0].axvspan(t_min, t_max, alpha=0.15)
            for _, row in grp[(grp['t']>=t_min)&(grp['t']<=t_max)].iterrows():
                axes[0].annotate(row['event'], (row['t'], row['ent_mean']),
                                 textcoords="offset points", xytext=(0,10),
                                 ha='center', fontsize=8, rotation=20)

            axes[1].errorbar(grp['t'], grp['x1_mean'], yerr=grp['x1_std'].fillna(0), fmt='-o', capsize=3)
            axes[1].set_ylabel('x1')
            axes[1].axvline(t_peak, linestyle='--', linewidth=1)
            axes[1].axvspan(t_min, t_max, alpha=0.15)

            axes[2].errorbar(grp['t'], grp['x2_mean'], yerr=grp['x2_std'].fillna(0), fmt='-o', capsize=3)
            axes[2].set_ylabel('x2')
            axes[2].axvline(t_peak, linestyle='--', linewidth=1)
            axes[2].axvspan(t_min, t_max, alpha=0.15)

            axes[3].errorbar(grp['t'], grp['alpha_mean'], yerr=grp['alpha_std'].fillna(0), fmt='-o', capsize=3)
            axes[3].set_ylabel('alpha')
            axes[3].set_xlabel('t (science event at t=0)')
            axes[3].axvline(t_peak, linestyle='--', linewidth=1)
            axes[3].axvspan(t_min, t_max, alpha=0.15)

            fig.suptitle(f"{ch}: Event annotations + x1/x2/alpha alongside entropy\n(peak band shaded; dashed = mean entropy peak)")
            fig.tight_layout(rect=[0,0,1,0.95])

            fig.savefig(out_fig_dir / f"{ch}_timeseries.png", dpi=160)
            pdf.savefig(fig)
            plt.close(fig)

            # Zoom plot (raw points)
            zoom = sub[sub['t'].between(t_min, t_max)]
            rng = np.random.default_rng(seed)
            t_jitter = zoom['t'].to_numpy() + rng.normal(scale=0.06, size=len(zoom))
            fig2, ax = plt.subplots(figsize=(10,4))
            ax.scatter(t_jitter, zoom['entropy'], s=12, alpha=0.7)
            ax.set_title(f"{ch}: Local zoom around entropy maximum (phase transition precursor)\nzoom t∈[{t_min},{t_max}]")
            ax.set_xlabel('t (jittered)')
            ax.set_ylabel('Entropy')
            ax.axvline(t_peak, linestyle='--', linewidth=1)
            for _, row in grp[(grp['t']>=t_min)&(grp['t']<=t_max)].iterrows():
                ax.annotate(row['event'], (row['t'], row['ent_mean']),
                            textcoords="offset points", xytext=(0,10),
                            ha='center', fontsize=8, rotation=20)
            fig2.tight_layout()
            fig2.savefig(out_fig_dir / "entropy_peak_zoom" / f"{ch}_entropy_peak_zoom.png", dpi=180)
            pdf.savefig(fig2)
            plt.close(fig2)

            meta[ch] = {'t_peak': t_peak, 'band': [t_min, t_max], 'n_points': int(len(sub))}

        # Summary page
        fig, ax = plt.subplots(figsize=(10,5))
        text = "\n".join([f"{ch}: peak t={meta[ch]['t_peak']}, band={meta[ch]['band']}, n={meta[ch]['n_points']}" for ch in sorted(meta.keys())])
        ax.axis('off')
        ax.text(0.01, 0.95, "Entropy peak bands per character", va='top', fontsize=14)
        ax.text(0.01, 0.85, text, va='top', fontsize=11)
        pdf.savefig(fig)
        plt.close(fig)

    return meta
