# src/monitoring_api/api/main.py
from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..pipeline import predict_from_json
from ..logging_utils import get_logger

logger = get_logger()

app = FastAPI(
    title="ZeroQ Monitoring API",
    description="SECOM 센서 기반 불량 탐지 관제용 예측 API",
    version="1.0.0",
)


class PredictRequest(BaseModel):
    payload: Dict[str, Any]


class PredictResponse(BaseModel):
    prob_defect: float
    pred_label: int
    threshold: float


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        result = predict_from_json(req.payload)
        return result
    except Exception as e:
        logger.exception("Prediction error")
        raise HTTPException(status_code=400, detail=str(e))