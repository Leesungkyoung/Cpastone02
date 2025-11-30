# src/backend/outliers.py

from typing import Dict, Any, List
import pandas as pd
import numpy as np

from . import data_access


def get_outlier_counts(label_col: str = "label") -> List[Dict[str, Any]]:
    """
    IQR 방식으로 각 sensor 컬럼별 이상치 개수 계산 (train 기준)
    - 이미 너가 만들어둔 함수 역할 그대로 유지
    """
    df = data_access.load_train()

    numeric_cols = [c for c in df.columns if c != label_col]

    outlier_info = []

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = ((df[col] < lower) | (df[col] > upper)).sum()

        outlier_info.append({
            "feature": col,
            "outliers": int(count)
        })

    return outlier_info


def get_outlier_summary(label_col: str = "label") -> Dict[str, Any]:
    """
    이상치 개수 요약 (탭2에서 쓸 수 있는 간단 요약)
    """
    info = get_outlier_counts(label_col=label_col)

    total_outliers = sum(d["outliers"] for d in info)
    n_features = len(info)

    # 이상치가 전혀 없는 컬럼 수
    zero_outlier_cols = sum(1 for d in info if d["outliers"] == 0)

    return {
        "n_features": n_features,
        "total_outliers": total_outliers,
        "zero_outlier_features": zero_outlier_cols,
        "detail": info,
    }


def get_outlier_boxplot_data(
    sensors: List[str] | None = None,
    label_col: str = "label",
) -> Dict[str, Any]:
    """
    탭4 상단 좌측 박스: IQR Before / After Boxplot용 데이터.

    - Before: raw 데이터 분포 (결측 포함, 극단값 포함)
    - After : train 데이터 분포 (전처리 후, IQR/mean/VIF 등 적용된 상태)

    반환 형태 예시:
    {
      "sensors": ["sensor_101", "sensor_102", ...],
      "before": {
          "sensor_101": [... 값 리스트 ...],
          ...
      },
      "after": {
          "sensor_101": [... 값 리스트 ...],
          ...
      }
    }
    """
    raw = data_access.load_raw()
    train = data_access.load_train()

    # label 컬럼 제외 센서 후보
    raw_features = [c for c in raw.columns if c != label_col]
    train_features = [c for c in train.columns if c != label_col]

    # raw와 train 둘 다 존재하는 센서만 사용
    common_features = [c for c in train_features if c in raw_features]

    # 프론트에서 센서 리스트를 안 넘겨주면, 앞에서부터 일부만 사용 (예: 20개)
    if sensors is None:
        sensors = common_features[:20]
    else:
        # 요청된 센서 중 실제 공통으로 존재하는 것만 필터
        sensors = [s for s in sensors if s in common_features]

    before_dict: Dict[str, list] = {}
    after_dict: Dict[str, list] = {}

    for col in sensors:
        before_vals = raw[col].dropna().tolist()
        after_vals = train[col].dropna().tolist()

        before_dict[col] = before_vals
        after_dict[col] = after_vals

    return {
        "sensors": sensors,
        "before": before_dict,
        "after": after_dict,
    }
