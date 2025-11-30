from sqlalchemy.orm import Session
from datetime import datetime
import json
import sqlite3
from sqlalchemy import or_

from backend import models
from backend import schemas

from sqlalchemy.orm import Session
from backend.models import Alert

# (1) Create Alert
def create_alert(db: Session, alert_data: dict):
    # The router ensures top_sensors is a JSON string.
    db_alert = models.Alert(
        timestamp=alert_data["timestamp"],
        product_id=alert_data["product_id"],
        top_sensors=alert_data["top_sensors"],
        prob=alert_data.get("prob"),
        resolved=alert_data.get("resolved", False),
        resolved_at=None
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

# (2) Get All Alerts
def get_alerts(db: Session):
    return db.query(models.Alert).order_by(models.Alert.id.desc()).all()

# (3) Resolve an Alert
def resolve_alert(db: Session, alert_id: int):
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if db_alert and not db_alert.resolved:
        db_alert.resolved = True
        db_alert.resolved_at = datetime.utcnow()
        db.commit()
        db.refresh(db_alert)
    return db_alert

# 데모 데이터 리셋을 위한 새로운 함수
def delete_demo_data(db: Session):
    """
    새로고침 시 금일 데모 스트리밍 데이터만 리셋합니다.
    - 2008-11-25 스트리밍 데이터 삭제
    - 2025년 등 현재 테스트 데이터 삭제
    - 과거 시드 데이터(7-10월, 11월 초)는 보존됩니다.
    """
    try:
        deleted_rows = (
            db.query(Alert)
            .filter(
                or_(
                    Alert.timestamp.like("2008-11-25%"), # Today's demo streaming data
                    Alert.timestamp.like("2025-%")      # Current year test data for development
                )
            )
            .delete(synchronize_session=False)
        )

        db.commit()
        if deleted_rows > 0:
            print(f"[DEMO RESET] Deleted {deleted_rows} session rows (2008-11-25, 2025-).")
        return {"status": "ok", "deleted_rows": deleted_rows}

    except Exception as e:
        db.rollback()
        print(f"[DEMO RESET ERROR] {e}")
        raise e