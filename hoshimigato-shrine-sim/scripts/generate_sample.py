"""Generate fictional sample data (CSV + JSON).

Usage:
  python scripts/generate_sample.py --outdir data
"""
import argparse, json, math, os
import numpy as np
import pandas as pd

def generate(seed=42, n=2000, dt=0.5, event_i0=1200, event_i1=1600):
    rng = np.random.default_rng(seed)
    t = np.arange(n) * dt
    idx = np.arange(n)
    event_mask = (idx >= event_i0) & (idx <= event_i1)

    base_mu, base_sigma, corr = 2.0, 0.5, 0.6
    cov = (base_sigma**2) * np.array([[1, corr, corr],[corr, 1, corr],[corr, corr, 1]])
    xyz = rng.multivariate_normal([base_mu]*3, cov, size=n)

    drift = 0.25*np.sin(2*np.pi*t/700) + 0.15*np.sin(2*np.pi*t/170)
    xyz += drift[:, None]

    outside_prob = 0.01
    hit = rng.random(n) < (outside_prob + 0.8 * event_mask.astype(float))
    amp = rng.lognormal(mean=math.log(20.0), sigma=0.6, size=n)
    direction = rng.normal(size=(n, 3))
    direction /= (np.linalg.norm(direction, axis=1, keepdims=True) + 1e-9)
    xyz[hit] += amp[hit, None] * direction[hit]

    df = pd.DataFrame({"t_sec": t, "X": xyz[:,0], "Y": xyz[:,1], "Z": xyz[:,2]})
    df["MAG"] = np.sqrt(df["X"]**2 + df["Y"]**2 + df["Z"]**2)
    df["temp"] = 22.0 - (1.8 * event_mask.astype(float)) + rng.normal(0, 0.05, size=n)
    df["phase"] = np.arctan2(df["Y"], df["X"])
    df["event_flag"] = event_mask.astype(int)
    df["terminal_id"] = "obs_terminal_2"
    df["location"] = "Hoshimigato Shrine"

    meta = {
        "seed": seed,
        "n_samples": int(n),
        "dt_sec": float(dt),
        "units": {"X": "mG", "Y": "mG", "Z": "mG", "MAG": "mG", "temp": "degC", "phase": "radians"},
        "event_window": {
            "sample_index_start": int(event_i0),
            "sample_index_end": int(event_i1),
            "t_start_sec": float(event_i0 * dt),
            "t_end_sec": float(event_i1 * dt),
            "note": "fictional anomaly window; event_flag==1"
        },
        "terminal": {"id": "obs_terminal_2", "location": "Hoshimigato Shrine"}
    }
    return df, meta

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="data")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df, meta = generate(seed=args.seed)

    csv_path = os.path.join(args.outdir, "hoshimigato_shrine_sample.csv")
    json_path = os.path.join(args.outdir, "hoshimigato_shrine_sample.json")

    df.to_csv(csv_path, index=False)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"metadata": meta, "records": df.to_dict(orient="records")}, f, ensure_ascii=False, indent=2)

    print("Wrote:")
    print(" -", csv_path)
    print(" -", json_path)

if __name__ == "__main__":
    main()
