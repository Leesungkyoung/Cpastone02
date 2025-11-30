from pathlib import Path

# capstone02_project 폴더를 기준 루트로 사용
BASE_DIR = Path(__file__).resolve().parent.parent

# === 디렉토리 경로 ===
DATA_DIR = BASE_DIR / "data" / "processed"   # capstone02_project/data/processed
MODEL_DIR = BASE_DIR / "models"              # capstone02_project/models

# ✅ 여기 수정/추가 부분
RESULTS_DIR = BASE_DIR / "results"           # capstone02_project/results
RESULT_DIR = RESULTS_DIR                     # 예전 코드 호환용 (둘 다 사용 가능)
