# src/monitoring_api/logging_utils.py
import logging
from logging import Logger

from .config import LOG_DIR


def get_logger(name: str = "monitoring_api") -> Logger:
    """
    관제 API 공용 로거.

    - results/logs/api.log 파일에 기록.
    - 동일 이름 로거를 여러 번 호출해도 핸들러는 중복 추가되지 않음.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_file = LOG_DIR / "api.log"
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )
    fh.setFormatter(fmt)

    logger.addHandler(fh)

    # 콘솔 출력도 함께 보고 싶다면 아래 주석 해제
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger