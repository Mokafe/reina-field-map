import argparse
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from hoshimigato import load_shrine_data, plot_shrine_dashboard

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to CSV or JSON sample data")
    ap.add_argument("--out", default=None, help="Optional output PNG path")
    args = ap.parse_args()

    df, meta = load_shrine_data(args.input)
    fig = plot_shrine_dashboard(df, meta)

    if args.out:
        fig.savefig(args.out, dpi=150, bbox_inches="tight")
        print(f"Saved: {args.out}")
    else:
        import matplotlib.pyplot as plt
        plt.show()

if __name__ == "__main__":
    main()
