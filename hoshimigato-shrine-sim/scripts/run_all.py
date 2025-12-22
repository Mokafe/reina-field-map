#!/usr/bin/env python3
"""
One-command pipeline for the story-to-ML dataset:

- Load CSV
- Export per-character "entropy peak band" teachcut
- Produce (entropy + x1/x2/alpha) plots with event annotations
- Fit a vanilla GMM (EM) on x1/x2 and plot overlay

Usage (from repo root):
  python scripts/run_all.py --data data/hoshike_all_data_en.csv
"""

from __future__ import annotations
import argparse
from pathlib import Path

from src.io import load_csv
from src.analysis import export_teachcut
from src.plotting import plot_character_bundle
from src.em_gmm import fit_and_plot_gmm_x1x2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=str, default="data/hoshike_all_data_en.csv")
    ap.add_argument("--out", type=str, default="outputs")
    ap.add_argument("--band_half_width", type=int, default=1)
    ap.add_argument("--gmm_components", type=int, default=6)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df = load_csv(args.data, translate_events=True)

    teachcut_path = export_teachcut(df, out_dir=out/"teachcut", band_half_width=args.band_half_width)
    print(f"[ok] teachcut written to: {teachcut_path}")

    pdf_path = out/"plots_en.pdf"
    fig_dir  = out/"figures"
    meta = plot_character_bundle(df, out_pdf=pdf_path, out_fig_dir=fig_dir, band_half_width=args.band_half_width)
    print(f"[ok] plots written to: {pdf_path}")

    gmm_df = fit_and_plot_gmm_x1x2(df, out_path=fig_dir/"gmm_overlay_x1x2.png", n_components=args.gmm_components)
    gmm_df.to_csv(out/"all_data_with_gmm_clusters.csv", index=False)
    print(f"[ok] gmm overlay written to: {fig_dir/'gmm_overlay_x1x2.png'}")

if __name__ == "__main__":
    main()
