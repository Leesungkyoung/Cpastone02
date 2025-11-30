# src/backend/diagnostics.py

import pandas as pd
from . import data_access


# ---------------------------------------
# 1) 기본 통계
# ---------------------------------------
def get_basic_stats(label_col: str = "label"):
    """
    train 데이터 기준 기본 통계(mean, std, min, max)
    label 컬럼은 제외하고 계산
    """
    df = data_access.load_train()

    numeric_cols = [c for c in df.columns if c != label_col]

    desc = df[numeric_cols].describe().T  # 테이블 형태로 전치
    desc = desc[["mean", "std", "min", "max"]]  # 필요한 컬럼만 선택

    return desc.reset_index().rename(columns={"index": "feature"}).to_dict(orient="records")


# ---------------------------------------
# 2) 결측치 분석
# ---------------------------------------
def get_missing_by_feature(label_col: str = "label"):
    """
    각 sensor 컬럼별 결측치 개수/비율 계산
    """
    df = data_access.load_train()

    numeric_cols = [c for c in df.columns if c != label_col]

    total_rows = len(df)

    summary = []
    for col in numeric_cols:
        miss = df[col].isna().sum()
        ratio = miss / total_rows
        summary.append({
            "feature": col,
            "missing": int(miss),
            "ratio": round(ratio, 4)
        })

    return summary


def get_missing_summary(label_col: str = "label"):
    """
    전체 결측 개수 + 컬럼 수 + 결측 있는 컬럼만 추출
    """
    df = data_access.load_train()

    total_missing = int(df.isna().sum().sum())
    missing_cols = df.columns[df.isna().sum() > 0].tolist()

    return {
        "total_missing": total_missing,
        "missing_columns": missing_cols,
    }
