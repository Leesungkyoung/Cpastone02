from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import settings as crud_settings
from typing import Optional
import json

router = APIRouter()

class AdminInfo(BaseModel):
    name: str
    department: str
    phone: str
    email: str
    photo_url: Optional[str] = None

class AdminSettings(BaseModel):
    monitor_admin: AdminInfo
    quality_manager: AdminInfo


@router.get("/settings/admins", response_model=AdminSettings)
def get_admin_settings(db: Session = Depends(get_db)):
    settings_json = crud_settings.get_setting(db, "admin_settings")
    if settings_json:
        return json.loads(settings_json.value)
    
    # Return default structure if not found
    default_info = {
        "name": "", "department": "", "phone": "", "email": "example@example.com", "photo_url": None
    }
    return AdminSettings(monitor_admin=default_info, quality_manager=default_info)


@router.put("/settings/admins", response_model=AdminSettings)
def update_admin_settings(settings: AdminSettings, db: Session = Depends(get_db)):
    settings_json_str = settings.model_dump_json()
    updated_setting = crud_settings.update_setting(db, "admin_settings", settings_json_str)
    return json.loads(updated_setting.value)
