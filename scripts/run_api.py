# scripts/run_api.py
import os
import sys

import uvicorn

# ─────────────────────────────────────────
# 1) src를 sys.path에 추가해서 monitoring_api 인식시키기
# ─────────────────────────────────────────
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))      # .../capstone02_project/scripts
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)                   # .../capstone02_project
SRC_DIR = os.path.join(PROJECT_ROOT, "src")                   # .../capstone02_project/src

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# 이제부터는 src/ 아래를 루트처럼 import 가능
from monitoring_api.api.main import app

# ─────────────────────────────────────────
# 2) Uvicorn으로 FastAPI 앱 실행
# ─────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,   # 필요하면 True로 바꿔도 됨 (개발용)
    )