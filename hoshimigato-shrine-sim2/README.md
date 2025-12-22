# Hoshimigato Shrine Simulation (story-to-ML)

This folder is a **Colab-friendly mini-project** that turns the *Hoshimigato* story world into a compact dataset for **EM/GMM** experimentation.

- **science event = t=0** (all characters align here)
- features: `x1`, `x2`, `alpha`, latent-ish `z`, and `entropy`
- includes 6 characters: **misaki / takumi / kurokawa / reina / aoi / tome**

## What’s inside

- `data/hoshike_all_data_en.csv` (main dataset; ~120 rows)
- `data/teachcut/teachcut_peak_band.csv` (only the *entropy-peak band* per character)
- `scripts/run_all.py` (one-command pipeline)
- `src/` (plot + EM/GMM helpers)
- `notebooks/` (Colab notebooks)

## Quick start (local)

```bash
pip install -r requirements.txt
python scripts/run_all.py --data data/hoshike_all_data_en.csv
```

Outputs will be written under `outputs/`:
- `outputs/plots_en.pdf` (event annotations + x1/x2/alpha alongside entropy, per character)
- `outputs/figures/gmm_overlay_x1x2.png` (EM/GMM overlay in x1-x2)
- `outputs/teachcut/teachcut_peak_band.csv` (peak-band cut)

## Quick start (Colab)

After you push this folder to GitHub, open the notebook:

- `notebooks/00_quickstart_colab.ipynb`

If you place this folder under:

- `Mokafe/reina-field-map/main/hoshimigato-shrine-sim/`

then your Colab URL will be:

```text
https://colab.research.google.com/github/Mokafe/reina-field-map/blob/main/hoshimigato-shrine-sim/notebooks/00_quickstart_colab.ipynb
```

## Notes

- Event text is translated into `event_en` for plotting, but the original `event` is kept.
- The “entropy peak band” is defined as `t_peak ± 1` (per character), then intersected with the character’s available `t`.

Generated on 2025-12-22.
