# src/monitoring_api/thresholds.py
from __future__ import annotations

import json
from typing import Dict

from .config import THRESHOLD_PATH


def get_threshold() -> float:
    with open(THRESHOLD_PATH, "r", encoding="utf-8") as f:
        data: Dict[str, float] = json.load(f)
    return float(data["threshold_value"])


def set_threshold(new_value: float) -> None:
    """
    threshold 값을 JSON 파일에 반영.
    운영 단계에서 threshold 튜닝할 때 사용 가능.
    """
    with open(THRESHOLD_PATH, "w", encoding="utf-8") as f:
        json.dump({"threshold_value": float(new_value)}, f, ensure_ascii=False, indent=2)