import sys
from pathlib import Path

# 프로젝트 루트를 PYTHONPATH에 추가
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


from src import (
    get_data_overview,
    get_feature_reduction_summary,
    get_feature_reduction_text,
)

print("=== 데이터 개요 ===")
print(get_data_overview())

print("\n=== 피처 감소 요약 ===")
print(get_feature_reduction_summary())

print("\n=== 설명 텍스트 ===")
print(get_feature_reduction_text())

from src.backend.summary import get_label_distribution
print("=== 라벨 분포 ===")
print(get_label_distribution())

