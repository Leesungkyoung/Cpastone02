# src/backend/importance.py

"""
Feature Importance 계산 모듈
- 모델 기반 중요도 (RandomForest, XGBoost, LightGBM 등)
- 또는 SHAP 기반 중요도 (향후 확장 가능)
"""

from typing import Dict, Any
import numpy as np
import pandas as pd

from . import data_access


def get_feature_importance(
    model_path: str = None,
    top_k: int = 20,
    label_col: str = "label"
) -> Dict[str, Any]:
    """
    전처리된 train 데이터를 불러오고,
    저장된 모델의 feature importance를 계산한다.

    - model_path: 학습된 모델 pickle 경로
    - top_k: 상위 중요도 K개
    - label_col: 라벨 컬럼 이름
    """

    # ==============================
    # 1. 전처리 데이터 로드
    # ==============================
    train = data_access.load_train()
    feature_cols = [c for c in train.columns if c != label_col]

    # ==============================
    # 2. 모델 기반 중요도 (model_path 제공된 경우)
    # ==============================
    if model_path is not None:
        try:
            import joblib
            model = joblib.load(model_path)

            # RandomForest / XGBoost / LightGBM 등
            if hasattr(model, "feature_importances_"):
                importances = model.feature_importances_
            else:
                raise AttributeError("모델에 feature_importances_ 속성이 없습니다.")

        except Exception as e:
            return {
                "error": f"모델 로드 중 오류 발생: {e}",
                "features": [],
                "importances": [],
                "top_features": [],
            }

    else:
        # ==============================
        # 3. 모델 없이 중요도 계산 (탭3 더미용)
        # ==============================
        # 각 feature 표준편차를 기반으로 임시 중요도 생성
        importances = train[feature_cols].std().values

    # ==============================
    # 4. 중요도 정규화
    # ==============================
    importances = np.array(importances, dtype=float)
    if importances.sum() > 0:
        importances = importances / importances.sum()

    # ==============================
    # 5. 중요도 내림차순 정렬
    # ==============================
    sorted_idx = np.argsort(importances)[::-1]

    sorted_features = [feature_cols[i] for i in sorted_idx]
    sorted_importance = importances[sorted_idx].tolist()

    # ==============================
    # 6. Top-K 추출
    # ==============================
    top_features = [
        {"feature": sorted_features[i], "importance": sorted_importance[i]}
        for i in range(min(top_k, len(sorted_features)))
    ]

    return {
        "features": sorted_features,
        "importances": sorted_importance,
        "top_features": top_features,
    }
