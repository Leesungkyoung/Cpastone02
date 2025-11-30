# src/backend/final_model.py
"""
Model Final 탭에서 사용할 최종 성능/곡선/혼동행렬 데이터를 넘겨주는 백엔드 모듈.

- 성능 값: Stage H 최종 모델 (Best F1 Threshold 기준)
- Baseline 값: metrics_summary_baseline(mean).csv 에서 선택한 조합
- Confusion Matrix: Stage H 최종 모델 TN, FP, FN, TP
"""

from __future__ import annotations
from typing import Dict, Any

import numpy as np
import pandas as pd

# =======================================================
# 1) Stage H 최종 성능 (너가 준 값 그대로)
# =======================================================
FINAL_METRICS = {
    "accuracy": 0.910828,
    "precision": 0.333333,
    "recall": 0.333333,
    "specificity": 0.952218,
    "f1": 0.333333,
    "balanced_accuracy": 0.642776,
    "roc_auc": 0.810011,
    "pr_auc": 0.226450,
    "tn": 279.0,
    "fp": 14.0,
    "fn": 14.0,
    "tp": 7.0,
}

# =======================================================
# 2) Baseline 성능 (metrics_summary_baseline(mean).csv 에서 선택한 조합)
#    Top-40 + SMOTE + LogisticRegression (F1 기준)
# =======================================================
BASELINE_METRICS = {
    "recall": 0.666667,
    "f1": 0.254545,
    "pr_auc": 0.238790,
    "roc_auc": 0.777994,
}

# Stage I Best F1 Threshold
BEST_F1_THRESHOLD = 0.6429997389333499


# =======================================================
# 3) KPI / 표 / 곡선 / 혼동행렬 생성 함수
# =======================================================
def _build_kpi() -> Dict[str, Any]:
    """
    백엔드용 KPI (지금은 프론트에서 직접 kpi를 만들고 있어서
    필수는 아니지만, 혹시 다른 곳에서 쓸 수 있으니 유지).
    """
    f = FINAL_METRICS
    b = BASELINE_METRICS

    return {
        "Threshold": BEST_F1_THRESHOLD,
        "Recall": {
            "Final": f["recall"],
            "Baseline": b["recall"],
        },
        "F1-Score": {
            "Final": f["f1"],
            "Baseline": b["f1"],
        },
        "AUC-PR": {
            "Final": f["pr_auc"],
            "Baseline": b["pr_auc"],
        },
        "AUC-ROC": {
            "Final": f["roc_auc"],
            "Baseline": b["roc_auc"],
        },
    }


def _build_metrics_table() -> pd.DataFrame:
    """Evaluation Metrics Table용 DataFrame."""
    f = FINAL_METRICS
    rows = [
        {"Metric": "Accuracy", "Value": f["accuracy"]},
        {"Metric": "Precision", "Value": f["precision"]},
        {"Metric": "Recall", "Value": f["recall"]},
        {"Metric": "F1 Score", "Value": f["f1"]},
        {"Metric": "Specificity (TN Rate)", "Value": f["specificity"]},
        {"Metric": "Balanced Accuracy", "Value": f["balanced_accuracy"]},
        {"Metric": "ROC-AUC", "Value": f["roc_auc"]},
        {"Metric": "PR-AUC", "Value": f["pr_auc"]},
        {"Metric": "TN", "Value": f["tn"]},
        {"Metric": "FP", "Value": f["fp"]},
        {"Metric": "FN", "Value": f["fn"]},
        {"Metric": "TP", "Value": f["tp"]},
    ]
    return pd.DataFrame(rows)


def _build_dummy_curves() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    PR/ROC curve 모양은 단순 더미로 생성.
    AUC 값 숫자 자체는 FINAL_METRICS를 프론트에서 사용.
    """
    # PR curve
    recall = np.linspace(0, 1, 50)
    precision = 1 - 0.8 * recall
    pr_df = pd.DataFrame({"recall": recall, "precision": precision})

    # ROC curve
    fpr = np.linspace(0, 1, 50)
    tpr = fpr ** 0.6
    roc_df = pd.DataFrame({"fpr": fpr, "tpr": tpr})

    return pr_df, roc_df


def _build_confusion_matrix() -> list[list[float]]:
    """2x2 혼동행렬 (TN, FP, FN, TP 순서)."""
    f = FINAL_METRICS
    cm = [
        [f["tn"], f["fp"]],
        [f["fn"], f["tp"]],
    ]
    # Streamlit에서 다루기 편하도록 list로 반환
    return cm


# =======================================================
# 4) 메인 진입 함수 (대시보드에서 호출)
# =======================================================
def get_final_dashboard_data() -> Dict[str, Any]:
    """
    pages/03_model_final.py 에서 사용하는 데이터 패키지.
    반드시 포함해야 하는 키:
      - "metrics_table"
      - "metrics"
      - "cm"
      - "pr_curve"
      - "roc_curve"
    (kpi는 지금은 프론트에서 직접 생성하지만, 혹시 모를 확장성을 위해 같이 넣어둔다.)
    """
    kpi = _build_kpi()
    metrics_table = _build_metrics_table()
    pr_curve, roc_curve = _build_dummy_curves()
    cm = _build_confusion_matrix()

    return {
        "kpi": kpi,
        "metrics_table": metrics_table,
        "metrics": metrics_table,
        "cm": cm,
        "pr_curve": pr_curve,
        "roc_curve": roc_curve,
    }
