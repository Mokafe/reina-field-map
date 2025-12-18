import json
import pandas as pd

def load_shrine_data(path: str):
    """Load sample data from CSV or JSON.

    JSON format is expected to be:
      { "metadata": {...}, "records": [ {row}, {row}, ... ] }

    Returns:
      df (pd.DataFrame), meta (dict)
    """
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
        meta = {}
    elif path.lower().endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        meta = obj.get("metadata", {})
        df = pd.DataFrame(obj["records"])
    else:
        raise ValueError("Please provide a .csv or .json file.")

    # light column fallbacks
    rename_map = {}
    for a, b in [("temp_C", "temp"), ("MAG_mG", "MAG"), ("X_mG", "X"), ("Y_mG", "Y"), ("Z_mG", "Z")]:
        if a in df.columns and b not in df.columns:
            rename_map[a] = b
    if rename_map:
        df = df.rename(columns=rename_map)

    required = ["t_sec", "X", "Y", "Z", "MAG", "temp", "phase"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df, meta
