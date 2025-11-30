from sqlalchemy.orm import Session
from ..models import Setting
import json

def get_setting(db: Session, key: str):
    return db.query(Setting).filter(Setting.key == key).first()

def update_setting(db: Session, key: str, value: str):
    db_setting = db.query(Setting).filter(Setting.key == key).first()
    if db_setting:
        db_setting.value = value
    else:
        db_setting = Setting(key=key, value=value)
        db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting
