from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd

from .logging_utils import get_logger

logger = get_logger(__name__)

SENSOR_PREFIX = "sensor_"


def parse_and_validate(json_payload: Dict[str, Any]) -> pd.DataFrame:
    """
    관제에서 들어온 JSON payload를 pandas DataFrame 으로 변환 + 기본 유효성 체크.

    허용 형식:
      1) {"payload": { "sensor_001": ..., "sensor_002": ..., ... }}
      2) {"sensor_001": ..., "sensor_002": ..., ...}  (flat 형식)

    정책:
      - key 가 "sensor_" 로 시작하는 것만 센서로 취급
      - value:
          * None / null         -> np.nan (전처리 단계에서 처리)
          * int / float         -> float
          * 숫자 형태의 문자열   -> float 로 변환 ("1.23" 등)
          * 빈 문자열("")       -> np.nan
          * 그 외 타입/문자열   -> 에러
    """
    # 1) payload 래핑 여부 처리
    if "payload" in json_payload and isinstance(json_payload["payload"], dict):
        data = json_payload["payload"]
    else:
        data = json_payload

    if not isinstance(data, dict):
        raise ValueError("payload 형식이 잘못되었습니다. dict 여야 합니다.")

    # 2) sensor_ 로 시작하는 키만 추출
    sensor_items = {
        str(k): v for k, v in data.items() if str(k).startswith(SENSOR_PREFIX)
    }

    if not sensor_items:
        raise ValueError("sensor_ 로 시작하는 센서 값이 하나도 없습니다.")

    parsed: Dict[str, float] = {}

    for key, value in sensor_items.items():
        # 2-1) None/null 은 허용 → np.nan 으로 넘김 (전처리에서 처리하기 위함)
        if value is None:
            parsed[key] = np.nan
            continue

        # 2-2) 숫자 타입 (int/float/np.number)
        if isinstance(value, (int, float, np.number)):
            parsed[key] = float(value)
            continue

        # 2-3) 문자열인 경우: 숫자 형태인지 체크
        if isinstance(value, str):
            v = value.strip()
            if v == "":
                parsed[key] = np.nan
                continue
            try:
                parsed[key] = float(v)
                continue
            except ValueError:
                raise ValueError(f"센서 값이 숫자가 아닙니다: {key}={value!r}")

        # 2-4) 그 외 타입은 에러
        else:
            raise ValueError(
                f"센서 값 타입이 잘못되었습니다: {key} type={type(value)} value={value!r}"
            )

    # 3) 단일 row DataFrame 생성
    df = pd.DataFrame([parsed])

    nan_ratio = float(df.isna().mean().mean())
    logger.info(
        "[schema] parse_and_validate 완료: shape=%s, nan_ratio=%.4f",
        df.shape,
        nan_ratio,
    )
    return df