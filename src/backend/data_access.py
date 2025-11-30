# src/backend/data_access.py

from pathlib import Path
from typing import Optional
import pandas as pd

# === 프로젝트 루트 / data 경로 설정 ===
# .../capstone02_project/src/backend/data_access.py 기준으로
# 부모 2번 올라가면 capstone02_project 폴더가 됨.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

# 원본 SECOM 데이터 폴더
RAW_SECOM_DIR = DATA_DIR / "raw" / "secom"
SECOM_FEATURES_FILE = RAW_SECOM_DIR / "secom.data"
SECOM_LABELS_FILE = RAW_SECOM_DIR / "secom_labels.data"

# 전처리 후 train 데이터
TRAIN_FILE = DATA_DIR / "secom_model_train.csv"

def load_raw() -> pd.DataFrame:
    """
    원본(master) SECOM 데이터 로딩.

    - features: raw/secom/secom.data  (590개 센서 컬럼)
    - labels  : raw/secom/secom_labels.data (label, timestamp ...)

    반환:
        센서 컬럼 + label 라벨이 붙은 DataFrame
    """
    if not SECOM_FEATURES_FILE.exists():
        raise FileNotFoundError(f"[load_raw] 특징 파일을 찾을 수 없습니다: {SECOM_FEATURES_FILE}")
    if not SECOM_LABELS_FILE.exists():
        raise FileNotFoundError(f"[load_raw] 라벨 파일을 찾을 수 없습니다: {SECOM_LABELS_FILE}")

    # secom.data: 공백 구분, 헤더 없음, 'NaN' 문자열을 결측으로 처리
    X = pd.read_csv(
        SECOM_FEATURES_FILE,
        sep=r"\s+",
        header=None,
        na_values=["NaN"],
    )

    X.columns = [f"sensor_{i+1}" for i in range(X.shape[1])]

    # secom_labels.data: 첫 번째 컬럼이 label, 나머지는 timestamp 관련
    y = pd.read_csv(
        SECOM_LABELS_FILE,
        sep=r"\s+",
        header=None,
    )
    label_series = y.iloc[:, 0]   # ✅ 첫 번째 컬럼만 label로 사용

    # 센서 + label 합치기
    df = X.copy()
    df["label"] = label_series.values

    return df

TRAIN_FILE = DATA_DIR / "processed" / "base_master_mean.parquet"

def load_train() -> pd.DataFrame:
    if not TRAIN_FILE.exists():
        raise FileNotFoundError(f"[load_train] train 파일 없음: {TRAIN_FILE}")
    return pd.read_parquet(TRAIN_FILE)


