# backend/services/preprocess.py
import numpy as np
import pandas as pd
import json
from pathlib import Path
from scipy.stats import zscore

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

# Load artifacts
with open(MODELS_DIR / "stageI_final_features.json", "r") as f:
    TOP40 = json.load(f)["feature_list"]

with open(MODELS_DIR / "sensors_mean_std_median.json", "r") as f:
    SENSOR_STATS = json.load(f)


def select_top40(raw_dict):
    """590개 raw 센서 중 Top40만 선택."""
    data = {k: raw_dict.get(k, np.nan) for k in TOP40}
    return pd.DataFrame([data])


def preprocess_top40(df: pd.DataFrame):
    """결측치 처리 + 이상치 완화 (mean / median)."""
    df = df.copy()
    for col in df.columns:
        mean_val = SENSOR_STATS[col]["mean"]
        median_val = SENSOR_STATS[col]["median"]
        std_val = SENSOR_STATS[col]["std"]

        # NaN → mean
        df[col] = df[col].fillna(mean_val)

        # 이상치 → median (Z-score > 3)
        if std_val > 0:
            z = abs((df[col] - mean_val) / std_val)
            df.loc[z > 3, col] = median_val

    return df


def create_features(df: pd.DataFrame):
    """파생변수 330개 생성."""
    df_fe = df.copy()

    # 1) 절대값/제곱/로그
    for col in df.columns:
        df_fe[f"{col}_abs"] = df[col].abs()
        df_fe[f"{col}_sq"] = df[col] ** 2
        df_fe[f"{col}_log"] = np.log1p(np.clip(df[col], a_min=0, a_max=None))

    # 2) 상위 10개 센서 조합 (차이/비율)
    top10 = TOP40[:10]
    for i in range(len(top10)):
        for j in range(i + 1, len(top10)):
            c1, c2 = top10[i], top10[j]
            df_fe[f"{c1}_minus_{c2}"] = df[c1] - df[c2]
            df_fe[f"{c1}_ratio_{c2}"] = df[c1] / (df[c2] + 1e-5)

    # 3) IQR flag / P95 flag
    for col in df.columns:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

        df_fe[f"{col}_iqr_flag"] = ((df[col] < lower) | (df[col] > upper)).astype(int)
        df_fe[f"{col}_p95_flag"] = (df[col] >= df[col].quantile(0.95)).astype(int)

    return df_fe