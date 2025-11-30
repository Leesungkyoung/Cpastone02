# src/backend/distribution.py

import pandas as pd
from . import data_access


def get_feature_distribution(feature: str, label_col: str = "label"):
    """
    특정 sensor(feature) 컬럼의 분포(히스토그램) 데이터 반환.

    반환 값:
    {
        "feature": "sensor_217",
        "values": [...],
        "min": float,
        "max": float,
        "mean": float,
        "std": float
    }
    """

    df = data_access.load_train()

    if feature not in df.columns:
        return {
            "feature": feature,
            "values": [],
            "min": None,
            "max": None,
            "mean": None,
            "std": None
        }

    # 값 목록 (라벨 제외)
    values = df[feature].dropna().tolist()

    return {
        "feature": feature,
        "values": values,
        "min": float(df[feature].min()),
        "max": float(df[feature].max()),
        "mean": float(df[feature].mean()),
        "std": float(df[feature].std())
    }
# src/backend/diagnostics.py  (기존 코드 아래에 추가)

def get_zscore_top10(
    threshold: float = 3.0,
    top_k: int = 10,
    label_col: str = "label",
):
    """
    탭4 상단 우측 - Z-score TOP 10 용 데이터.

    - 기준: |Z| > threshold 인 값의 개수가 많은 센서 순으로 정렬
    - train 데이터 기준 (전처리 이후)
    """
    df = data_access.load_train()

    feature_cols = [c for c in df.columns if c != label_col]
    X = df[feature_cols]

    # 평균, 표준편차
    means = X.mean()
    stds = X.std().replace(0, np.nan)  # 표준편차 0이면 NaN 처리해서 제외

    # Z-score 계산
    z = (X - means) / stds

    # 이상치(|Z| > threshold) 개수
    outlier_counts = (z.abs() > threshold).sum(axis=0)

    total_rows = len(X)

    rows = []
    for feat, cnt in outlier_counts.items():
        if np.isnan(cnt):
            continue
        ratio = (cnt / total_rows) if total_rows > 0 else 0.0
        rows.append({
            "feature": feat,
            "outlier_count": int(cnt),
            "outlier_ratio": float(round(ratio, 4)),
        })

    # 이상치 개수 기준 내림차순 정렬
    rows_sorted = sorted(rows, key=lambda x: x["outlier_count"], reverse=True)

    return {
        "threshold": threshold,
        "total_rows": total_rows,
        "scores": rows_sorted,
        "top_k": top_k,
        "top_features": rows_sorted[:top_k],
    }


def get_high_missing_columns(
    threshold: float = 0.4,
    label_col: str = "label",
):
    """
    탭4 상단 우측 - 결측률 ≥ 0.4 컬럼 제거 리스트용 데이터.

    - raw 데이터 기준으로 결측률 계산
    - train에 남아있는지 여부(is_removed_in_train)도 같이 반환
    """
    raw = data_access.load_raw()
    train = data_access.load_train()

    total_rows = len(raw)
    raw_features = [c for c in raw.columns if c != label_col]
    train_features = set([c for c in train.columns if c != label_col])

    miss_counts = raw[raw_features].isna().sum()
    miss_ratios = miss_counts / total_rows

    result = []
    for feat in raw_features:
        ratio = float(miss_ratios[feat])
        if ratio >= threshold:
            result.append({
                "feature": feat,
                "missing_count": int(miss_counts[feat]),
                "missing_ratio": float(round(ratio, 4)),
                "is_removed_in_train": (feat not in train_features),
            })

    # 결측률 기준 내림차순
    result_sorted = sorted(result, key=lambda x: x["missing_ratio"], reverse=True)

    return {
        "threshold": threshold,
        "total_features": len(raw_features),
        "n_high_missing": len(result_sorted),
        "columns": result_sorted,
    }
