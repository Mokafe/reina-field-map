# Hoshimigato Shrine Simulation（story-to-ML / 物語→機械学習）

このフォルダは、小説世界 *Hoshimigato* を **EM / GMM（EMアルゴリズム）実験用のコンパクトなデータセット**に落とし込むための、
**Colab-friendly mini-project** です。

- **science event = t=0**（全キャラがここで時間合わせ）
- features: `x1`, `x2`, `alpha`, latent-ish `z`, `entropy`
- characters: **misaki / takumi / kurokawa / reina / aoi / tome**

> Note: このリポジトリには `hoshimigato-shrine-sim` と `hoshimigato-shrine-sim2` のように  
> 同プロジェクトの複製が入る場合があります（GitHub Web UI での誤上書き回避のため）。  
> **ノートブックはどちらのフォルダでも動く設計**です。

---

## Open in Colab（クリックで起動）

> ↓ これが **sim2 用の直リンク**です（このREADMEが置かれているフォルダを前提）

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](
https://colab.research.google.com/github/Mokafe/reina-field-map/blob/main/hoshimigato-shrine-sim2/notebooks/00_quickstart_colab.ipynb
)

---

## 収録物（What’s inside）

- `data/hoshike_all_data_en.csv`  
  メインデータ（約120行 / ~120 rows）
- `data/teachcut/teachcut_peak_band.csv`  
  各キャラの **エントロピー極大帯（entropy-peak band）**だけを切り出した教材用データ
- `scripts/run_all.py`  
  ワンコマンド実行パイプライン（one-command pipeline）
- `src/`  
  plot + EM/GMM helpers
- `notebooks/`  
  Colab notebooks

---

## まず何が出る？（Outputs）

実行すると `outputs/` に以下が生成されます：

- `outputs/plots_en.pdf`  
  キャラごとに **イベント注釈 + entropy + x1/x2/alpha 並走**をまとめたPDF
- `outputs/figures/gmm_overlay_x1x2.png`  
  `x1-x2` 平面での **GMM（EM）重ね描き**
- `outputs/teachcut/teachcut_peak_band.csv`  
  教材用：**entropy極大（相転移直前）周辺の t 帯**だけを切り出したCSV

---

## Quick start（local）

このフォルダ内で実行します：

```bash
pip install -r requirements.txt
python scripts/run_all.py --data data/hoshike_all_data_en.csv
