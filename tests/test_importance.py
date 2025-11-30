# tests/test_importance.py

import sys
from pathlib import Path

# ─────────────────────────────────
# ① 프로젝트 루트를 sys.path에 추가
#   (src 패키지를 찾을 수 있게 해줌)
# ─────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.backend.importance import get_feature_importance


if __name__ == "__main__":
    print("=== Feature Importance 테스트 ===")

    # 모델 경로는 아직 안 쓰고, 표준편차 기반 더미 중요도로 테스트
    result = get_feature_importance(model_path=None, top_k=10)

    print("\n상위 10개 중요 피처:")
    for item in result["top_features"]:
        print(f"- {item['feature']}: {item['importance']:.4f}")
