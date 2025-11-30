# src/monitoring_api/pipeline.py
from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np
import pandas as pd

from .artifacts import load_artifacts
from .features import build_features_from_raw
from .logging_utils import get_logger
from .schema import parse_and_validate

logger = get_logger()

# API 모듈의 엔진

# 애플리케이션 시작 시 한 번만 artifact 로드
# main.py 에서도 load_artifacts() 를 호출하지만,
# 여기서도 호출해서 전역 변수에 저장해 둠
_MODEL, _SCALER, _THRESHOLD, _CORE_FEATURE_LIST, _FULL_FEATURE_LIST = load_artifacts()

logger.info(
    f"Artifacts loaded: threshold={_THRESHOLD}, "
    f"core_feature_list_len={0 if _CORE_FEATURE_LIST is None else len(_CORE_FEATURE_LIST)}, "
    f"full_feature_list_len={0 if _FULL_FEATURE_LIST is None else len(_FULL_FEATURE_LIST)}"
)


def _prepare_input_matrix(df_features: pd.DataFrame) -> np.ndarray:
    """
    df_features 를 모델 입력 형태의 numpy 배열로 변환.

    - FULL feature 리스트(_FULL_FEATURE_LIST)가 존재하면
      그 순서에 맞게 reindex (StageG/StageH 학습 시점의 컬럼 구조와 동일하게 맞춤)
    """
    if _FULL_FEATURE_LIST is not None:
        missing = [c for c in _FULL_FEATURE_LIST if c not in df_features.columns]
        if missing:
            # 완전히 똑같이 맞추는 게 베스트지만,
            # 혹시 빠진 게 있으면 NaN 컬럼으로 채워넣고 경고만 띄움
            logger.warning(
                f"모델이 기대하는 full feature 중 누락된 컬럼이 있습니다. "
                f"예시 missing={missing[:5]} (총 {len(missing)}개)"
            )

        df_features = df_features.reindex(columns=_FULL_FEATURE_LIST)

    X = df_features.to_numpy().astype("float32")
    return X


def predict_from_json(json_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    관제 JSON payload → 예측 결과까지 한 번에 수행하는 코어 함수.

    Parameters
    ----------
    json_payload : Dict[str, Any]
        관제 시스템에서 전송한 센서 데이터 JSON

    Returns
    -------
    result : Dict[str, Any]
        {
            "prob_defect": float,  # 불량일 확률
            "pred_label": int,     # 0(정상) / 1(불량)
            "threshold": float
        }
    """
    logger.info(f"Received payload keys: {list(json_payload.keys())}")

    # 1) JSON 파싱 & 유효성 검사
    df_raw = parse_and_validate(json_payload)

    # 2) 전처리 + 파생 피처 생성
    df_features = build_features_from_raw(df_raw) #df_fe를 여기서 받음

    # 3) 스케일링
    X = _prepare_input_matrix(df_features)
    X_scaled = _SCALER.transform(X)

    # 4) 예측 확률 (양성 클래스 기준)
    if hasattr(_MODEL, "predict_proba"):
        prob = float(_MODEL.predict_proba(X_scaled)[0, 1])
    elif hasattr(_MODEL, "decision_function"):
        # decision_function 출력값을 시그모이드로 변환 (예비용)
        score = float(_MODEL.decision_function(X_scaled)[0])
        prob = 1.0 / (1.0 + np.exp(-score))
    else:
        # 이진 예측만 가능한 모델인 경우,
        # 일단 0/1 예측 후, 그 값을 확률처럼 사용
        pred_raw = int(_MODEL.predict(X_scaled)[0])
        prob = float(pred_raw)

    # 5) threshold 로 최종 라벨 결정
    pred_label = int(prob >= _THRESHOLD)

    result: Dict[str, Any] = {
        "prob_defect": prob,
        "pred_label": pred_label,
        "threshold": float(_THRESHOLD),
    }

    logger.info(f"Prediction result: {result}")
    return result