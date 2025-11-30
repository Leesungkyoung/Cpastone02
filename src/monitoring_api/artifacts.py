from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Tuple

import joblib

from .config import MODEL_DIR
from .logging_utils import get_logger

logger = get_logger(__name__)

# 예측 모델이랑 스케일링 돌리는 파일

# 모델/스케일러/threshold/feature 리스트 파일 경로
FULL_FEATURE_LIST_PATH = MODEL_DIR / "stageI_full_feature_list.json"    #추가
MODEL_PATH = MODEL_DIR / "stageI_final_lgbm_model.pkl"
SCALER_PATH = MODEL_DIR / "stageI_final_scaler.pkl"
THRESHOLD_PATH = MODEL_DIR / "stageI_final_threshold.json"
FEATURE_LIST_PATH = MODEL_DIR / "stageI_final_features.json"


def _load_model(path: Path = MODEL_PATH):
    if not path.exists():
        raise FileNotFoundError(f"[artifacts] 모델 파일을 찾을 수 없습니다: {path}")
    logger.info(f"[artifacts] 모델 로딩: {path}")
    model = joblib.load(path)
    return model


def _load_scaler(path: Path = SCALER_PATH):
    if not path.exists():
        raise FileNotFoundError(f"[artifacts] 스케일러 파일을 찾을 수 없습니다: {path}")
    logger.info(f"[artifacts] 스케일러 로딩: {path}")
    scaler = joblib.load(path)
    return scaler


def _load_threshold(path: Path = THRESHOLD_PATH) -> float:
    """
    threshold JSON에서 threshold_value 값 로드.
    없으면 기본값 0.5 사용.
    """
    if not path.exists():
        logger.warning(
            f"[artifacts] threshold 파일이 없습니다. 기본값 0.5 를 사용합니다: {path}"
        )
        return 0.5

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # {"threshold_value": 0.64} 형태를 기대
    if isinstance(data, dict) and "threshold_value" in data:
        thr = float(data["threshold_value"])
        logger.info(f"[artifacts] threshold 로딩 완료: {thr}")
        return thr

    # 숫자 하나만 있는 경우도 허용
    if isinstance(data, (int, float)):
        thr = float(data)
        logger.info(f"[artifacts] threshold(숫자) 로딩 완료: {thr}")
        return thr

    logger.warning(
        f"[artifacts] threshold JSON 형식이 이상합니다. data={str(data)[:200]} "
        "→ 기본값 0.5 사용"
    )
    return 0.5


def _load_feature_list(path: Path = FEATURE_LIST_PATH) -> Optional[List[str]]:
    """
    stageI_final_features.json 이 존재하면 피처 이름 리스트를 로드.
    없으면 None 반환(= DataFrame 컬럼 순서를 그대로 사용).

    지원 포맷:
      1) {"features": [...]}         ← 기존 버전
      2) {"feature_list": [...]}     ← 지금 탱볼이가 만든 버전
      3) [..., ...]                  ← 리스트 그대로 저장된 버전
    """
    if not path.exists():
        logger.info(f"[artifacts] feature 리스트 파일이 없습니다: {path}")
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Case 1 — {"features": [...]}
    if isinstance(data, dict) and "features" in data:
        features = data["features"]

    # Case 2 — {"feature_list": [...]}
    elif isinstance(data, dict) and "feature_list" in data:
        features = data["feature_list"]

    # Case 3 — 그냥 리스트
    elif isinstance(data, list):
        features = data

    else:
        logger.warning(
            "[artifacts] feature 리스트 JSON 형식이 올바르지 않습니다. "
            f"type={type(data)}, data_preview={str(data)[:200]}"
        )
        return None

    if not isinstance(features, list):
        logger.warning(
            "[artifacts] feature 리스트는 리스트여야 합니다. "
            f"type={type(features)}"
        )
        return None

    features = [str(col) for col in features]
    logger.info(f"[artifacts] feature 리스트 로딩 완료 (len={len(features)})")
    return features

# 추가
def _load_full_feature_list(path: Path = FULL_FEATURE_LIST_PATH) -> Optional[List[str]]:
    """
    StageG / StageH 최종 파생피처까지 포함된 full feature 리스트 로드.

    stageI_full_feature_list.json 형식:
      { "features": ["sensor_042", "sensor_332", ...] }
    """
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "features" in data:
        features = data["features"]
    else:
        features = data

    if not isinstance(features, list):
        raise ValueError("[artifacts] full feature 리스트 JSON 형식이 올바르지 않습니다.")

    return [str(col) for col in features]

from typing import Any, List, Optional, Tuple

def load_artifacts() -> Tuple[Any, Any, float, Optional[List[str]], Optional[List[str]]]:
    """
    모델, 스케일러, threshold, core feature 리스트(40개), full feature 리스트(329개)를 함께 로드.
    """
    model = _load_model()
    scaler = _load_scaler()
    threshold = _load_threshold()

    core_feature_list = _load_feature_list()         # stageI_final_features.json (40개)
    full_feature_list = _load_full_feature_list()    # stageI_full_feature_list.json (329개)

    logger.info(
        "[artifacts] Artifacts loaded: "
        f"threshold={threshold}, "
        f"core_feature_list_len={0 if core_feature_list is None else len(core_feature_list)}, "
        f"full_feature_list_len={0 if full_feature_list is None else len(full_feature_list)}"
    )
    return model, scaler, threshold, core_feature_list, full_feature_list