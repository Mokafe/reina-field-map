import matplotlib.pyplot as plt

def plot_shrine_dashboard(df, meta=None, title_suffix="(Chapter 7)"):
    """Plot a 3-panel dashboard:
    1) EMF magnitude with detection window
    2) Temperature (cold spot)
    3) Phase scatter colored by magnitude
    """
    # detection window
    t0 = t1 = None
    if "event_flag" in df.columns and (df["event_flag"] == 1).any():
        t0 = df.loc[df["event_flag"] == 1, "t_sec"].min()
        t1 = df.loc[df["event_flag"] == 1, "t_sec"].max()
    elif meta and "event_window" in meta:
        t0 = meta["event_window"].get("t_start_sec")
        t1 = meta["event_window"].get("t_end_sec")

    fig, axes = plt.subplots(3, 1, figsize=(15, 10), sharex=True)
    plt.subplots_adjust(hspace=0.4)

    # (1) EMF magnitude
    ax1 = axes[0]
    ax1.plot(df["t_sec"], df["MAG"], color="#4B0082", lw=1, label="EMF Magnitude (mG)")
    if t0 is not None and t1 is not None:
        ax1.axvspan(t0, t1, color="red", alpha=0.10, label="Detection Window")
    ax1.set_title(f"Hoshimigato Shrine - Sensor Log {title_suffix}")
    ax1.set_ylabel("Strength (mG)")
    ax1.legend(loc="upper right")

    # (2) Temperature
    ax2 = axes[1]
    ax2.plot(df["t_sec"], df["temp"], color="#0000FF", lw=1.5)
    ax2.set_ylabel("Temp (°C)")
    ax2.set_title("Environmental: Cold Spot Detection")

    # (3) Phase scatter
    ax3 = axes[2]
    sc = ax3.scatter(df["t_sec"], df["phase"], c=df["MAG"], cmap="twilight", s=2, alpha=0.6)
    ax3.set_ylabel("Phase (radians)")
    ax3.set_title("Field Phase Analysis (Complex Plane Mapping)")
    ax3.set_xlabel("Time (sec)")
    cbar = fig.colorbar(sc, ax=ax3, pad=0.01)
    cbar.set_label("EMF Magnitude (mG)")

    return fig
