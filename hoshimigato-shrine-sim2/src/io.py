"""
I/O helpers for the Hoshimigato story-to-ML dataset.

Data schema (CSV):
t,x1,x2,alpha,z,entropy,character,event,event_en
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import pandas as pd

EVENT_EN_MAP = {
    '研究所での通常業務': 'Routine lab work',
    '研究推進': 'Research push',
    '支配強化': 'Control tightens',
    '広報資料作成指示': 'PR deck assignment',
    '感情はノイズと再確認': 'Reaffirms "emotion is noise"',
    '自主実験開始': 'Starts independent field experiment',
    '陰口を聴く': 'Overhears gossip',
    '独白ログ': "Writes soliloquy log",
    '独白ログ発見': "Finds Takumi's log",
    '鬼火に巻き込まれる': "Ensnared by will-o'-wisps",
    '夢を見る': 'Has a dream (premonition)',
    '同行決意': 'Decides to go together',
    'トメがレイナの電話を受ける': "Tome answers Reina's call",
    '冷めてもいいようにまんじゅうを作る': 'Makes manju for his return',
    '破綻兆候': 'Signs of breakdown',
    '内的揺らぎ': 'Inner wobble begins',
    '村の大人への根回し': 'Pre-briefs the villagers',
    '裁判所条件調整': 'Tunes "courtroom condition" code',
    '裏からの介入決断': 'Decides to intervene from behind',
    '裁判所突入': 'Enters the Court of Light',
    '裁判所で選択': 'Makes a choice in the Court of Light',
    '救助の兆しを感じる': 'Detects a rescue signal',
    '救助の段取りを整える': 'Arranges the rescue plan',
    '現実側支援': 'Support from the real side',
    '生還': 'Found alive',
    '帰還': 'Returns',
    '回復支援': 'Supports recovery',
    '日常の回復を見守る': 'Watches daily life recover',
    '価値転換': 'Value shift',
    '退職と技術再定義': 'Resigns & redefines the tech',
}

def load_csv(path: str | Path, translate_events: bool = True) -> pd.DataFrame:
    df = pd.read_csv(path)
    if translate_events:
        if 'event_en' not in df.columns:
            df['event_en'] = df['event'].map(EVENT_EN_MAP).fillna(df['event'])
    return df
