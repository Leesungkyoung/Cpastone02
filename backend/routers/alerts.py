from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import ast # ast 모듈 추가

from backend import schemas
from backend.database import get_db
from backend.crud import alerts as alerts_crud

router = APIRouter()

def convert_db_alert(db_alert):
    """DB Alert 객체를 Pydantic 모델로 변환하고, top_sensors 파싱을 안전하게 처리합니다."""
    sensors = []
    if db_alert.top_sensors:
        try:
            # 1. 유효한 JSON으로 파싱 시도
            sensors = json.loads(db_alert.top_sensors)
        except json.JSONDecodeError:
            try:
                # 2. 실패 시, Python 리스트 문자열로 안전하게 평가
                sensors = ast.literal_eval(db_alert.top_sensors)
            except (ValueError, SyntaxError):
                # 두 방법 모두 실패 시 빈 리스트로 처리 (또는 에러 로깅)
                sensors = []
    
    return schemas.AlertResponse(
        id=db_alert.id,
        timestamp=db_alert.timestamp.isoformat(),
        product_id=db_alert.product_id,
        top_sensors=sensors,
        prob=db_alert.prob,
        resolved=db_alert.resolved,
        resolved_at=db_alert.resolved_at.isoformat() if db_alert.resolved_at else None,
    )


@router.post("/alerts", response_model=schemas.AlertResponse)
def create_alert_endpoint(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    data = alert.dict()
    # top_sensors를 항상 JSON 문자열로 저장하도록 보장
    data['top_sensors'] = json.dumps(data.get('top_sensors', []))

    db_alert = alerts_crud.create_alert(db=db, alert_data=data)
    return convert_db_alert(db_alert)

@router.get("/alerts", response_model=List[schemas.AlertResponse])
def get_alerts_endpoint(db: Session = Depends(get_db)):
    db_alerts = alerts_crud.get_alerts(db)
    return [convert_db_alert(alert) for alert in db_alerts]

@router.patch("/alerts/{alert_id}/resolve", response_model=schemas.AlertResponse)
def resolve_alert_endpoint(alert_id: int, db: Session = Depends(get_db)):
    db_alert = alerts_crud.resolve_alert(db=db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return convert_db_alert(db_alert)