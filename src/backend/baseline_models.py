# src/backend/baseline_models.py
from typing import Dict


def get_model_summaries() -> Dict[str, dict]:
    """
    Baseline 탭에서 사용할 Model A / Model B 요약 정보를 반환합니다.
    - Model A : Median Imputation + RobustScaler (로버스트 설정)
    - Model B : Mean Imputation + StandardScaler (기존 설정)
    """
    return {
        "Model A": {
            "scaling": "RobustScaler",
            "model_type": "LogisticRegression",
            "pipeline": "Median Imputation → Robust Scaling → Feature Top-40 선택",
            "strength": (
                "이상치에 덜 민감하여 센서 분포가 치우친 환경에서도 성능이 안정적입니다. "
                "재학습 시 스케일 변화에 강인해 로버스트한 Baseline 모델로 활용 가능합니다."
            ),
            "limitation": (
                "평균 정보를 활용하지 않아 완만한 변동을 세밀하게 반영하는 데는 다소 불리할 수 있으며, "
                "RobustScaler 사용으로 StandardScaler 대비 해석이 직관적이지 않을 수 있습니다."
            ),
        },
        "Model B": {
            "scaling": "StandardScaler",
            "model_type": "LogisticRegression",
            "pipeline": "Mean Imputation → Standard Scaling → Feature Top-40 선택",
            "strength": (
                "구조가 단순하고 계산 비용이 적으며, 선형 관계 해석에 매우 용이합니다. "
                "평균·분산 기반 StandardScaler를 사용해 해석이 직관적입니다."
            ),
            "limitation": (
                "이상치에 민감하여 센서 값에 큰 튀는 값이 존재할 때 성능이 불안정해질 수 있고, "
                "복잡한 비선형 관계를 충분히 표현하는 데 한계가 있습니다."
            ),
        },
    }
