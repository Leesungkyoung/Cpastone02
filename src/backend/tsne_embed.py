# src/backend/tsne_embed.py

from typing import Dict, Any
import numpy as np
import pandas as pd

from . import data_access


def get_tsne_embedding(
    n_components: int = 2,
    perplexity: float = 30.0,
    random_state: int = 42,
    label_col: str = "label",
) -> Dict[str, Any]:
    """
    탭4 하단 – t-SNE 차원축소 결과.

    반환 예시:
    {
      "params": {...},
      "n_samples": 1567,
      "points": [
         {"index": 0, "tsne1": ..., "tsne2": ..., "label": 0},
         ...
      ]
    }
    """
    from sklearn.manifold import TSNE  # scikit-learn 필요

    df = data_access.load_train()

    if label_col not in df.columns:
        raise ValueError(f"label_col '{label_col}' not found in train data")

    X = df.drop(columns=[label_col])
    y = df[label_col].tolist()

    tsne = TSNE(
        n_components=n_components,
        perplexity=perplexity,
        random_state=random_state,
        init="random",
        learning_rate="auto",
    )
    emb = tsne.fit_transform(X.values)

    points = []
    for idx, (coord, label) in enumerate(zip(emb, y)):
        points.append({
            "index": int(idx),
            "tsne1": float(coord[0]),
            "tsne2": float(coord[1]) if n_components > 1 else 0.0,
            "label": int(label),
        })

    return {
        "params": {
            "n_components": n_components,
            "perplexity": perplexity,
            "random_state": random_state,
        },
        "n_samples": len(points),
        "points": points,
    }
