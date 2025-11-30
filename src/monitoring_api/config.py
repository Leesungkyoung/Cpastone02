# src/monitoring_api/config.py
from pathlib import Path

# 일종의 경로 설명서 역할을 하는 설정 파일

# 이 파일 위치: <PROJECT_ROOT>/src/monitoring_api/config.py
# 따라서 두 단계 위가 프로젝트 루트
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

# 모델, 스케일러, threshold, feature list 등이 저장된 디렉토리
MODEL_DIR: Path = PROJECT_ROOT / "models"

from pathlib import Path

# config.py 위치: <PROJECT_ROOT>/src/monitoring_api/config.py
# 두 단계 위가 프로젝트 루트
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

# 모델 디렉토리
MODEL_DIR: Path = PROJECT_ROOT / "models"

# 각 sensor별 mean&std&median의 저장되어있는 파일 경로
SENSOR_STATS_PATH: Path = MODEL_DIR / "sensors_mean_std_median.json"

# threshold 값이 들어 있는 JSON 파일 경로
THRESHOLD_PATH: Path = MODEL_DIR / "stageI_final_threshold.json"

# (선택) 최종 학습에 사용한 피처 리스트 JSON 경로
# 예: ["sensor_001", "sensor_002", ...]
FEATURE_LIST_PATH: Path = MODEL_DIR / "stageI_final_features.json"

# 로그 파일 디렉토리
LOG_DIR: Path = PROJECT_ROOT / "results" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 관제에서 들어올 센서 prefix
SENSOR_PREFIX: str = "sensor_"

# 타임스탬프 필드 이름
TIMESTAMP_FIELD: str = "timestamp"