from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from collections import Counter
import pandas as pd

def mode(series) -> str:
    if len(series) == 0:
        return ""
    return Counter(series).most_common(1)[0][0]

@dataclass
class PeakBand:
    character: str
    t_peak: float
    t_min: float
    t_max: float

def compute_peak_bands(df: pd.DataFrame, band_half_width: int = 1) -> dict[str, PeakBand]:
    """
    Peak band = [t_peak - band_half_width, t_peak + band_half_width] intersected with available t's.
    """
    out: dict[str, PeakBand] = {}
    for ch, sub in df.groupby('character'):
        # prefer mean entropy per t for peak selection
        grp = sub.groupby('t')['entropy'].mean().reset_index()
        t_peak = float(grp.loc[grp['entropy'].idxmax(), 't'])
        t_min = float(sub['t'].min())
        t_max = float(sub['t'].max())
        t0 = max(t_min, t_peak - band_half_width)
        t1 = min(t_max, t_peak + band_half_width)
        out[ch] = PeakBand(ch, t_peak, float(t0), float(t1))
    return out

def export_teachcut(df: pd.DataFrame, out_dir: str | Path, band_half_width: int = 1) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    bands = compute_peak_bands(df, band_half_width=band_half_width)
    chunks = []
    for ch, band in bands.items():
        sub = df[(df['character'] == ch) & (df['t'].between(band.t_min, band.t_max))]
        sub.to_csv(out_dir / f"{ch}_peak_band.csv", index=False)
        chunks.append(sub)
    teachcut = pd.concat(chunks, ignore_index=True)
    out_path = out_dir / "teachcut_peak_band.csv"
    teachcut.to_csv(out_path, index=False)
    return out_path
