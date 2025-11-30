# src/backend/model_ab.py
import pandas as pd
from pathlib import Path
from typing import Dict


def get_feature_importance_top40() -> Dict[str, pd.DataFrame]:
    """
    StageC에서 생성된 feature_frequency_*_top40.csv를 사용해서
    Lasso(Mean) / RandomForest(Median) Top-40 중요도 정보를 반환한다.
    - importance_lasso : feature, count, stability, importance
    - importance_rf    : feature, count, stability, importance
    """
    # model_ab.py → backend → src → capstone02_project
    BASE_DIR = Path(__file__).resolve().parents[2]
    RESULTS_DIR = BASE_DIR / "results" / "stageC"

    # ✅ 파일 경로 (이름 그대로 사용)
    lasso_path = RESULTS_DIR / "feature_frequency_mean_top40.csv"
    rf_path    = RESULTS_DIR / "feature_frequency)_median_top40.csv"

    # CSV 읽기
    importance_lasso = pd.read_csv(lasso_path)
    importance_rf    = pd.read_csv(rf_path)

    # 컬럼: feature, count, stability 가 있다고 가정
    # → count를 중요도 지표로 그대로 사용
    importance_lasso["importance"] = importance_lasso["count"]
    importance_rf["importance"]    = importance_rf["count"]

    return {
        "lasso": importance_lasso,
        "rf": importance_rf,
    }

def get_stability_scores() -> pd.DataFrame:
    """
    StageC에서 저장한 feature_frequency_*_top40.csv 파일을 사용하여
    Lasso / RandomForest 안정성(stability) 점수 분포를 반환한다.
    - Lasso : feature_frequency_mean_top40.csv  → stability 컬럼
    - RF    : feature_frequency)_median_top40.csv → stability 컬럼
    """
    # 1) 파일 경로 설정
    BASE_DIR = Path(__file__).resolve().parents[2]
    RESULTS_DIR = BASE_DIR / "results" / "stageC"

    lasso_path = RESULTS_DIR / "feature_frequency_mean_top40.csv"
    rf_path    = RESULTS_DIR / "feature_frequency)_median_top40.csv"  # 실제 파일명 그대로 사용

    # 2) CSV 로드
    df_lasso = pd.read_csv(lasso_path)
    df_rf    = pd.read_csv(rf_path)

    # (선택) 디버깅용 길이 출력
    print("[DEBUG] len(df_lasso):", len(df_lasso), "len(df_rf):", len(df_rf))
    print("[DEBUG] len(stability_lasso):", len(df_lasso["stability"]),
          "len(stability_rf):", len(df_rf["stability"]))

    # 3) 두 쪽 중 더 짧은 길이를 기준으로 사용
    n = min(len(df_lasso["stability"]), len(df_rf["stability"]))

    # 4) 그 길이(n)까지만 잘라서 DataFrame 생성
    stability_df = pd.DataFrame({
        "Lasso": df_lasso["stability"].values[:n],
        "RandomForest": df_rf["stability"].values[:n],
    })

    # 5) (선택) 0~1 범위로 클리핑
    stability_df = stability_df.clip(0, 1)

    return stability_df

from pathlib import Path
import pandas as pd

def load_baseline_metrics():
    """
    Baseline(Model A/B) 성능 CSV를 서로 다른 경로에서 불러오기
    """

    # Model A CSV 경로
    path_a = Path(
        r"C:\Users\seo58\OneDrive\바탕 화면\capstone02_project_final\capstone02_project\results\final\metrics_summary_baseline.csv"
    )

    # Model B CSV 경로
    path_b = Path(
        r"C:\Users\seo58\OneDrive\바탕 화면\capstone02_project(성경)\capstone02_project\results\final\metrics_summary_baseline.csv"
    )

    df_a = pd.read_csv(path_a)
    df_b = pd.read_csv(path_b)

    return {
        "Model A": df_a,
        "Model B": df_b,
    }
