from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import reports as crud_reports
from typing import Optional

router = APIRouter()

@router.get("/reports/summary")
def get_reports_summary(
    period_type: str = "monthly",
    month: Optional[str] = None, # "YYYY-MM"
    db: Session = Depends(get_db)
):
    try:
        summary_data = crud_reports.get_summary_data(db, period_type, month)
        return summary_data
    except Exception as e:
        # Log the error e for debugging
        print(f"Error fetching summary data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
