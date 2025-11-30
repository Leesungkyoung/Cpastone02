# backend/routers/predict.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.pipeline import run_prediction

router = APIRouter()

class PredictInput(BaseModel):
    timestamp: str
    product_id: int
    sensors: dict  # sensor_001 ~ sensor_590

class PredictOutput(BaseModel):
    product_id: int
    timestamp: str
    prob: float
    pred: int
    top_sensors: list

@router.post("/predict", response_model=PredictOutput)
def predict(data: PredictInput):

    result = run_prediction(data.sensors)

    return {
        "timestamp": data.timestamp,
        "product_id": data.product_id,
        "prob": result["prob"],
        "pred": result["pred"],
        "top_sensors": result["top_sensors"],
    }