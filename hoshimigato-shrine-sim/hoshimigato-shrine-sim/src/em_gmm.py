from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy.linalg as LA
from sklearn.mixture import GaussianMixture

def _plot_gmm_ellipses(ax, gmm: GaussianMixture):
    for mean, cov in zip(gmm.means_, gmm.covariances_):
        cov2 = cov[:2,:2] if cov.shape[0] > 2 else cov
        vals, vecs = LA.eigh(cov2)
        order = vals.argsort()[::-1]
        vals = vals[order]
        vecs = vecs[:, order]
        theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))
        width, height = 2*np.sqrt(vals)  # 1-sigma
        ell = patches.Ellipse(xy=mean[:2], width=width, height=height, angle=theta,
                              fill=False, linewidth=2)
        ax.add_patch(ell)
        ax.scatter(mean[0], mean[1], marker='x', s=80)

def fit_and_plot_gmm_x1x2(
    df: pd.DataFrame,
    out_path: str | Path,
    n_components: int = 6,
    seed: int = 42
) -> pd.DataFrame:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    X = df[['x1','x2']].to_numpy()
    gmm = GaussianMixture(n_components=n_components, covariance_type='full', random_state=seed, n_init=10)
    gmm.fit(X)
    labels = gmm.predict(X)

    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(df['x1'], df['x2'], c=labels, s=20, alpha=0.75)
    ax.set_xlabel('x1'); ax.set_ylabel('x2')
    ax.set_title(f'EM/GMM overlay in (x1,x2) space ({n_components} components)')
    _plot_gmm_ellipses(ax, gmm)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)

    out_df = df.copy()
    out_df['gmm_cluster'] = labels
    return out_df
