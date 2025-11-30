# backend/services/shap_utils.py
import re
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"


def extract_sensor_name(feature_name: str):
    """파생변수명을 sensor_XXX로 변환."""
    sensors = re.findall(r"(sensor_\d+)", feature_name)
    return sensors  # 리스트 반환


def select_top_sensors(feature_importances, feature_names, top_k=3):
    """
    feature_importances: np.array (330개)
    feature_names: list (330개)
    """
    fi_df = pd.DataFrame({
        "feature": feature_names,
        "importance": feature_importances
    })

    fi_df = fi_df.sort_values(by="importance", ascending=False)

    sensor_score = {}

    for _, row in fi_df.iterrows():
        sensors = extract_sensor_name(row["feature"])
        for s in sensors:
            sensor_score[s] = sensor_score.get(s, 0) + row["importance"]

    sensor_ranked = sorted(sensor_score.items(), key=lambda x: x[1], reverse=True)

    return [s[0] for s in sensor_ranked[:top_k]]