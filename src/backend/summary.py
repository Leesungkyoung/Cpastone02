# src/backend/summary.py

from typing import Dict, Any, List

import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from . import data_access
from src.config import DATA_DIR


def get_data_overview(label_col: str = "label") -> Dict[str, Any]:
    """
    탭1 상단 박스용 데이터 요약.
    - raw: 원본(master) 데이터
    - train: 전처리 완료(train) 데이터
    """
    raw = data_access.load_raw()
    train = data_access.load_train()

    raw_rows, raw_cols = raw.shape
    tr_rows, tr_cols = train.shape

    raw_missing = int(raw.isna().sum().sum())
    tr_missing = int(train.isna().sum().sum())

    def _safe_label_counts(df):
        return df[label_col].value_counts().to_dict() if label_col in df.columns else {}

    return {
        "raw": {
            "rows": raw_rows,
            "cols": raw_cols,
            "missing": raw_missing,
            "label_counts": _safe_label_counts(raw),
        },
        "train": {
            "rows": tr_rows,
            "cols": tr_cols,
            "missing": tr_missing,
            "label_counts": _safe_label_counts(train),
        },
    }


def get_label_distribution(label_col: str = "label") -> Dict[str, Any]:
    """
    탭1 하단 도넛 차트용 라벨 분포 데이터 (train 기준)
    """
    train = data_access.load_train()

    if label_col not in train.columns:
        return {"labels": [], "counts": [], "ratios": [], "total": 0}

    vc = train[label_col].value_counts().sort_index()

    labels = vc.index.tolist()
    counts = vc.values.tolist()
    total = int(vc.sum())
    ratios = [round(c / total, 4) for c in counts] if total > 0 else [0 for _ in counts]

    return {
        "labels": labels,
        "counts": counts,
        "ratios": ratios,
        "total": total,
    }


def get_feature_reduction_summary(label_col: str = "label") -> Dict[str, Any]:
    """
    원본(raw) vs 전처리(train) 기준 피처 수 비교.
    """
    raw = data_access.load_raw()
    train = data_access.load_train()

    # 라벨 컬럼 제외한 '센서 컬럼'만 비교
    raw_features = [c for c in raw.columns if c != label_col]
    tr_features = [c for c in train.columns if c != label_col]

    raw_set = set(raw_features)
    tr_set = set(tr_features)

    # 원본 중 최종 train에서 사용된 센서
    used_features = sorted(raw_set & tr_set)
    # 원본 중 제거된 센서
    removed_features = sorted(raw_set - tr_set)

    total_features = len(raw_features)
    final_features = len(used_features)
    n_removed = len(removed_features)
    removed_ratio = (n_removed / total_features) if total_features > 0 else 0.0

    return {
        "total_features": total_features,
        "final_features": final_features,
        "n_removed": n_removed,
        "removed_ratio": removed_ratio,
        "removed_features": removed_features,
        "used_features": used_features,
    }


def get_feature_reduction_text(label_col: str = "label") -> str:
    """
    피처 감소 요약 텍스트 (대시보드 상단 설명용)
    """
    info = get_feature_reduction_summary(label_col=label_col)

    total = info["total_features"]
    final = info["final_features"]
    n_removed = info["n_removed"]
    removed_ratio = info["removed_ratio"] * 100

    return (
        f"원본 센서 {total}개 중 전처리 후 {final}개를 사용하고 있습니다. "
        f"(총 {n_removed}개, {removed_ratio:.1f}% 센서가 제거됨)"
    )


def get_raw_and_clean(label_col: str = "label"):
    """
    Streamlit Summary 페이지에서 raw_data, clean_data 둘 다 필요할 때 호출하는 함수.
    raw  = data_access.load_raw()
    clean = data_access.load_train()
    """
    raw = data_access.load_raw()
    clean = data_access.load_train()

    # 라벨 존재 여부 체크
    if label_col not in clean.columns:
        raise KeyError(
            f"[get_raw_and_clean] '{label_col}' 컬럼이 clean 데이터에 없습니다. 실제 라벨 컬럼명을 확인하세요."
        )

    return raw, clean


def get_low_variance_and_vif_info(using: str = "mean") -> Dict[str, Any]:
    """
    preprocess_log_mean.json을 읽어서
    프론트에서 쓰는 각종 key 이름들을 전부 포함해서 반환한다.
    (all_sensors, after_missing, low_variance_removed, ... 등)
    """

    log_path = DATA_DIR / f"preprocess_log_{using}.json"
    with open(log_path, "r", encoding="utf-8") as f:
        log = json.load(f)

    # JSON에서 정보 꺼내기
    dropped_missing: List[str] = log.get("dropped_missing_cols", [])
    dropped_lowvar:  List[str] = log.get("dropped_lowvar", [])
    dropped_corr:    List[str] = log.get("dropped_corr", [])
    dropped_vif:     List[str] = log.get("dropped_vif", [])

    # SECOM 기준 전체 센서 리스트 (1~590)
    all_raw_sensors = [f"sensor_{i:03d}" for i in range(1, 591)]

    # 1단계: 결측비율 drop 이후
    after_missing = [s for s in all_raw_sensors if s not in dropped_missing]

    # 2단계: 저분산 drop 이후
    after_lowvar = [s for s in after_missing if s not in dropped_lowvar]

    # 3단계: 상관관계 filter 이후
    after_corr = [s for s in after_lowvar if s not in dropped_corr]

    # 4단계: VIF 이후
    after_vif = [s for s in after_corr if s not in dropped_vif]

    # alias 포함해서 모두 반환
    return {
        # ── 전체 센서 ──
        "all_sensors": all_raw_sensors,

        # ── Missing 단계 ──
        "before_missing": all_raw_sensors,
        "after_missing": after_missing,
        "removed_missing": dropped_missing,
        "missing_removed": dropped_missing,
        "dropped_missing": dropped_missing,

        # ── Low Variance 단계 ──
        "before_lowvar": after_missing,
        "after_lowvar": after_lowvar,
        "after_low_variance": after_lowvar,
        "removed_lowvar": dropped_lowvar,
        "low_variance_removed": dropped_lowvar,
        "lv_removed": dropped_lowvar,
        "dropped_lowvar": dropped_lowvar,

        # ── Correlation 단계 ──
        "before_corr": after_lowvar,
        "after_corr": after_corr,
        "removed_corr": dropped_corr,
        "corr_removed": dropped_corr,
        "dropped_corr": dropped_corr,

        # ── VIF 단계 ──
        "before_vif": after_corr,
        "after_vif": after_vif,
        "removed_vif": dropped_vif,
        "vif_removed": dropped_vif,
        "dropped_vif": dropped_vif,
    }


def get_feature_importance(label_col: str = "label", top_k: int = 19) -> pd.DataFrame:
    """
    전처리 완료(train) 데이터를 이용해서
    RandomForest 기반 Feature Importance를 계산해서 반환.
    """
    train = data_access.load_train()  # secom_model_train: 네 진짜 데이터

    X = train.drop(columns=[label_col])
    y = train[label_col]

    rf = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced_subsample",
    )
    rf.fit(X, y)

    importances = pd.Series(rf.feature_importances_, index=X.columns)
    imp_df = (
        importances.sort_values(ascending=False)
        .head(top_k)
        .reset_index()
    )
    imp_df.columns = ["feature", "importance"]
    return imp_df

# src/backend/summary.py

import pandas as pd
import numpy as np

def get_corr_filtering_info(corr_threshold: float = 0.95):
    """
    실제 SECOM 데이터 기준 상관관계 기반 피처 필터링 결과를 반환.
    - corr_threshold 보다 큰 상관관계를 가지는 컬럼 중 일부를 제거.
    반환:
        {
          'before_cols': [...],
          'after_cols': [...],
          'removed_cols': [...],
          'threshold': float
        }
    """
    # 1) 마스터 데이터 로드 (Stage B에서 쓰는 전처리된 파일 경로 사용)
    #    config 쪽에 정의된 경로에 맞춰서 수정해줘.
    #    예시: config.DATA_MASTER_MEAN 처럼 되어 있을 수도 있음.
    master_path = "C:/Users/seo58/OneDrive/바탕 화면/capstone02_project_final/capstone02_project/data/processed/base_master_mean.parquet" # 네 config.py에 맞게 이름 확인!
    df = pd.read_parquet(master_path)

    # 2) 센서 컬럼만 선택 (label 제외)
    sensor_cols = [c for c in df.columns if c != "label"]
    X = df[sensor_cols]

    # 3) 상관계수 행렬 계산 (절대값)
    corr = X.corr().abs()

    # 4) 상관관계 기반 제거 컬럼 선택
    to_drop = set()
    cols = corr.columns

    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            if corr.iloc[i, j] > corr_threshold:
                # 뒤쪽(j)을 제거 대상으로 넣음
                to_drop.add(cols[j])

    after_cols = [c for c in sensor_cols if c not in to_drop]
    removed_cols = sorted(list(to_drop))

    return {
        "before_cols": sensor_cols,
        "after_cols": after_cols,
        "removed_cols": removed_cols,
        "threshold": corr_threshold,
    }
def get_feature_filter_summary(using: str = "mean") -> Dict[str, int]:
    """
    preprocess_log_mean.json 기반으로
    상관관계 / VIF 전후 센서 개수를 요약해서 반환한다.

    반환 예:
    {
        "sensors_before_corr": 120,
        "sensors_after_corr": 80,
        "sensors_before_vif": 80,
        "sensors_after_vif": 60,
    }
    """
    info = get_low_variance_and_vif_info(using=using)

    # get_low_variance_and_vif_info가 이미 리스트를 다 만들어주고 있음
    before_corr = info["before_corr"]   # 상관관계 필터 전 센서 리스트
    after_corr = info["after_corr"]     # 상관관계 필터 후 센서 리스트
    before_vif = info["before_vif"]     # VIF 전 센서 리스트
    after_vif = info["after_vif"]       # VIF 후 센서 리스트

    return {
        "sensors_before_corr": len(before_corr),
        "sensors_after_corr": len(after_corr),
        "sensors_before_vif": len(before_vif),
        "sensors_after_vif": len(after_vif),
    }
