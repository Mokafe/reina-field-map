# Hoshimigato Shrine Simulation (story-to-ML)

This folder is a **Colab-friendly mini-project** that turns the *Hoshimigato* story world into a compact dataset for **EM/GMM** experimentation.

- **science event = t=0** (all characters align here)
- features: `x1`, `x2`, `alpha`, latent-ish `z`, and `entropy`
- includes 6 characters: **misaki / takumi / kurokawa / reina / aoi / tome**

> Note: This repo may contain multiple copies of this project folder (e.g., `hoshimigato-shrine-sim` and `hoshimigato-shrine-sim2`) to avoid accidental overwrites when uploading via GitHub Web UI.
> The Colab notebook is designed to work with either one.

---

## What’s inside

- `data/hoshike_all_data_en.csv` (main dataset; ~120 rows)
- `data/teachcut/teachcut_peak_band.csv` (only the *entropy-peak band* per character)
- `scripts/run_all.py` (one-command pipeline)
- `src/` (plot + EM/GMM helpers)
- `notebooks/` (Colab notebooks)

---

## Quick start (local)

From inside this folder:

```bash
pip install -r requirements.txt
python scripts/run_all.py --data data/hoshike_all_data_en.csv

