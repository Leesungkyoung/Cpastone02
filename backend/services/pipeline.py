# backend/services/pipeline.py
import pickle
import json
import numpy as np
from pathlib import Path

from backend.services.preprocess import (
    select_top40,
    preprocess_top40,
    create_features,
)
from backend.services.shap_utils import select_top_sensors

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

# Load artifacts
with open(MODELS_DIR / "stageI_final_features.json", "r") as f:
    TOP40 = json.load(f)["feature_list"]

with open(MODELS_DIR / "stageI_full_feature_list.json", "r") as f:
    FINAL_FEATURES = json.load(f)["features"]

with open(MODELS_DIR / "stageI_final_threshold.json", "r") as f:
    THRESHOLD = json.load(f)["threshold_value"]

with open(MODELS_DIR / "sensors_mean_std_median.json", "r") as f:
    SENSOR_STATS = json.load(f)

# 계속 에러나서 이거 수정함 
from joblib import load
SCALER = load(MODELS_DIR / "stageI_final_scaler.pkl")
MODEL = load(MODELS_DIR / "stageI_final_lgbm_model.pkl")


def run_prediction(raw_dict):
    """raw → Top40 → 전처리 → 파생변수 → 스케일링 → 예측 → top_sensors"""

    # 1️⃣ Top40 선택
    df40 = select_top40(raw_dict)

    # 2️⃣ 전처리
    df_clean = preprocess_top40(df40)

    # 3️⃣ 파생변수 생성 → 330개
    df_fe = create_features(df_clean)

    # 3-1) 최종 모델에 사용된 329개 변수만 순서대로 선택
    df_final = df_fe[FINAL_FEATURES]

    # 4️⃣ 스케일링
    X_scaled = SCALER.transform(df_final.values)

    # 5️⃣ 모델 예측
    y_prob = MODEL.predict_proba(X_scaled)[0][1]
    y_pred = int(y_prob >= THRESHOLD)

    # 6️⃣ 중요 센서 계산
    fi = MODEL.feature_importances_
    top_sens = select_top_sensors(fi, df_final.columns)

    return {
        "prob": float(y_prob),
        "pred": y_pred,
        "top_sensors": top_sens,
    }