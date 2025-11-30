from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd

from .logging_utils import get_logger
from .artifacts import _load_feature_list  # core feature 리스트 로더 재사용

import json
from pathlib import Path

# 수정; # from .config import SENSOR_STATS_PATH <- 이렇게 해도 됨
PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATS_PATH = PROJECT_ROOT / "models" / "sensors_mean_std_median.json"

with open(STATS_PATH, "r", encoding="utf-8") as f:
    SENSOR_STATS = json.load(f)


logger = get_logger(__name__)


# --------------------------------------------------------------
# 1. core feature 선택 + 숫자형 정리
# --------------------------------------------------------------
def select_core_features_from_raw(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    1단계: raw DataFrame 에서 최종 core feature 들만 선택하고 float32 로 정리.

    - StageH 에서 저장한 stageI_final_features.json 의 리스트를 artifacts.py 에서 로딩
    - raw 데이터 중 해당 컬럼들만 추출 (없으면 NaN 컬럼 생성)
    - 숫자형으로 변환 (to_numeric, errors='coerce') 후 float32 로 캐스팅
    """
    if not isinstance(df_raw, pd.DataFrame):
        raise TypeError(
            f"[features] select_core_features_from_raw 는 DataFrame 만 받을 수 있습니다. "
            f"type={type(df_raw)}"
        )

    core_features = _load_feature_list()  # artifacts.py 의 로더 재사용

    if core_features is None:
        # fallback: sensor_ 로 시작하는 컬럼 전부 사용
        sensor_cols: List[str] = [
            col for col in df_raw.columns if str(col).startswith("sensor_")
        ]
        logger.warning(
            "[features] core feature 리스트가 없어 sensor_* 컬럼 전체를 사용합니다. "
            f"cols={len(sensor_cols)}"
        )
        df_sel = df_raw[sensor_cols].copy()
    else:
        # 누락된 컬럼은 NaN 컬럼으로 채워서 생성
        missing = [c for c in core_features if c not in df_raw.columns]
        if missing:
            logger.warning(
                "[features] raw 데이터에 존재하지 않는 core feature 가 있습니다. "
                f"missing={missing[:5]} (총 {len(missing)}개)"
            )
        df_sel = pd.DataFrame(index=df_raw.index)
        for col in core_features:
            if col in df_raw.columns:
                df_sel[col] = df_raw[col]
            else:
                df_sel[col] = np.nan

    # 숫자형 변환 + float32 캐스팅
    for col in df_sel.columns:
        df_sel[col] = pd.to_numeric(df_sel[col], errors="coerce")

    df_sel.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_sel = df_sel.astype("float32")

    nan_ratio = float(df_sel.isna().mean().mean())
    logger.info(
        "[features] core feature 선택 및 numeric 정리 완료: "
        f"shape={df_sel.shape}, nan_ratio={nan_ratio:.4f}"
    )
    return df_sel


# --------------------------------------------------------------
# 2. mean 버전 전처리 (NaN 대치 + Z-score 기반 이상치 → median 대치)
# --------------------------------------------------------------
def preprocess_mean_version(
    df: pd.DataFrame,
    z_threshold: float = 3.0,
    stats_dict: dict | None = None,
) -> pd.DataFrame:
    """
    2단계: mean 버전 전처리 (온라인/실시간용).

    03_build_master_mean.ipynb 과 동일한 로직을 재현:

      1) NaN 을 학습 단계에서 계산한 각 컬럼의 mean 으로 대치
      2) Z-score 기준(|z| > Z_THRESHOLD) 이상치들을
         학습 단계에서 계산한 median 값으로 대치

    여기서 mean/std/median 은
    models/sensors_mean_std_median.json 에서 불러온 값을 사용한다.

    * 주의:
      - 온라인 추론에서는 feature_set 이 이미 고정이므로
        컬럼 드롭(결측률, 저분산, 상관도, VIF, IQR 드랍 등)은 수행하지 않는다.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"[features] preprocess_mean_version 는 DataFrame 만 받을 수 있습니다. "
            f"type={type(df)}"
        )

    # 통계 딕셔너리 설정 (외부에서 주입 가능, 기본은 글로벌 SENSOR_STATS 사용)
    if stats_dict is None:
        stats_dict = SENSOR_STATS

    X = df.copy()

    # --------------------------------------------------
    # 1) mean 대치 (학습 시 저장해둔 mean 사용)
    # --------------------------------------------------
    nan_before = int(X.isna().sum().sum())

    if nan_before > 0:
        for col in X.columns:
            if not X[col].isnull().any():
                continue

            # JSON에서 mean 가져오기 시도
            mean_val = None
            if stats_dict is not None and col in stats_dict:
                mean_val = stats_dict[col].get("mean", None)

            # 그래도 못 찾으면 현재 데이터 기준 mean fallback
            if mean_val is None or pd.isna(mean_val):
                mean_val = X[col].mean()

            # chained-assignment 방지: inplace 대신 대입
            X[col] = X[col].fillna(mean_val)

    nan_after = int(X.isna().sum().sum())
    logger.info(
        "[features] mean 대치 완료: "
        f"NaN before={nan_before}, NaN after={nan_after}"
    )

    # --------------------------------------------------
    # 2) Z-score 기반 이상치 완화 (|z| > threshold → median 대치)
    #    z 계산할 때도 stats_dict에 저장된 mean/std 사용
    # --------------------------------------------------
    replaced_total = 0

    for col in X.columns:
        # stats_dict에 해당 컬럼 정보가 없으면 스킵
        if stats_dict is None or col not in stats_dict:
            continue

        col_stats = stats_dict[col]
        col_mean = col_stats.get("mean", None)
        col_std = col_stats.get("std", None)
        col_median = col_stats.get("median", None)

        # std가 0이거나 결측이면 Z-score 의미 없으므로 스킵
        if col_std is None or col_std == 0 or pd.isna(col_std):
            continue
        if col_mean is None or pd.isna(col_mean):
            continue

        # 학습 분포 기준 Z-score 계산
        z = (X[col] - col_mean) / col_std
        mask = z.abs() > z_threshold

        if not mask.any():
            continue

        # median이 JSON에 없다면, 마지막 fallback으로 현재 데이터 기준 median
        if col_median is None or pd.isna(col_median):
            col_median = X[col].median()

        X.loc[mask, col] = col_median
        replaced_total += int(mask.sum())

    logger.info(
        "[features] Z-score 이상치 완화 완료: "
        f"총 대치된 값 개수={replaced_total}, Z_THRESHOLD={z_threshold}"
    )

    return X.astype("float32")



# --------------------------------------------------------------
# 3. StageG 파생 피처 (절대값/제곱/로그/차이/비율/IQR/p95)
#    → StageG_feature_engineering.ipynb 로직 최대한 그대로 재현
# --------------------------------------------------------------
def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    3단계: StageG_feature_engineering.ipynb 의 파생 피처를 재현.

    포함 내용:
      - 절대값 파생: col_abs
      - 제곱 파생: col_sq
      - 로그 파생: col_log (양수값 기준 log1p, 전체 데이터셋 기준 조건)
      - 중요 상위 10개 센서 간 차이/비율: c1_minus_c2, c1_ratio_c2
      - IQR 기반 이상치 플래그: col_iqr_flag
      - 상위 95% 이상 플래그: col_p95_flag
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"[features] add_engineered_features 는 DataFrame 만 받을 수 있습니다. "
            f"type={type(df)}"
        )

    if df.empty:
        logger.warning("[features] 입력 DataFrame 이 비어 있어 파생 피처 없이 반환합니다.")
        return df

    # 여기서 df 는 이미 core 40개 + 전처리(mean/Z-score)까지 끝난 상태라고 가정
    X = df.copy()
    X_fe = X.copy()

    # ----- 3-1. 절대값 파생 -----
    for col in X.columns:
        X_fe[f"{col}_abs"] = np.abs(X[col])

    # ----- 3-2. 제곱 파생 -----
    for col in X.columns:
        X_fe[f"{col}_sq"] = X[col] ** 2

    # ----- 3-3. 로그 파생 (양수만 대상) -----
    # StageG 노트북과 동일하게, "데이터셋 전체 기준 양수 값이 1개 이상" 이면 log 컬럼 생성
    for col in X.columns:
        col_values = X[col]
        # 한 row 만 들어와도, 값이 양수면 로그 피처 생성
        if (col_values > 0).sum() > 0:
            clipped = np.clip(col_values, a_min=0, a_max=None)
            X_fe[f"{col}_log"] = np.log1p(clipped)

    # ----- 3-4. 중요 상위 10개 센서만 조합 (차이/비율) -----
    top_k = 10
    important_cols = list(X.columns[:top_k])

    for i in range(len(important_cols)):
        for j in range(i + 1, len(important_cols)):
            c1, c2 = important_cols[i], important_cols[j]
            X_fe[f"{c1}_minus_{c2}"] = X[c1] - X[c2]
            X_fe[f"{c1}_ratio_{c2}"] = X[c1] / (X[c2] + 1e-5)

    # ----- 3-5. IQR 기반 이상치 플래그 -----
    # StageG 코드처럼 조건 없이 항상 flag 컬럼 생성
    for col in X.columns:
        series = X[col]
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        X_fe[f"{col}_iqr_flag"] = ((series < lower) | (series > upper)).astype(int)

    # ----- 3-6. 상위 95% 이상 플래그 -----
    for col in X.columns:
        series = X[col]
        p95 = series.quantile(0.95)
        X_fe[f"{col}_p95_flag"] = (series >= p95).astype(int)

    logger.info(
        "[features] 파생 피처 생성 완료: "
        f"원본 컬럼 수={X.shape[1]}, 파생 포함 후 컬럼 수={X_fe.shape[1]}"
    )
    return X_fe


# --------------------------------------------------------------
# 최종 오케스트레이터: pipeline 에서 이 함수만 호출
# --------------------------------------------------------------
def build_features_from_raw(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    관제에서 들어온 raw DataFrame → 모델/학습용 feature DataFrame 변환.

    내부 단계:
      1) select_core_features_from_raw: core feature 선택 + numeric 정리
      2) preprocess_mean_version: mean 대치 + Z-score 이상치 완화
      3) add_engineered_features: StageG 파생 피처 생성

    반환:
      - 모델/스케일러에 바로 넣을 수 있는 feature DataFrame
      - 실제 추론 시에는 pipeline 에서 feature_list 에 맞춰 최종 컬럼을 선택/정렬한다.
    """
    logger.info(f"[features] build_features_from_raw 시작: raw_shape={df_raw.shape}")

    df_core = select_core_features_from_raw(df_raw)
    df_pre = preprocess_mean_version(df_core)
    df_fe = add_engineered_features(df_pre)

    logger.info(f"[features] build_features_from_raw 완료: final_shape={df_fe.shape}")
    return df_fe