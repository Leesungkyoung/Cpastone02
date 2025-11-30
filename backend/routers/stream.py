# backend/routers/stream.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.stream import load_stream_rows
from ..crud.alerts import delete_demo_data

router = APIRouter()

@router.delete("/reset_demo", dependencies=[Depends(get_db)])
def reset_demo(db: Session = Depends(get_db)):
    result = delete_demo_data(db)
    return result

@router.get("/stream/all_rows")
def get_all_stream_rows():
    """
    Returns all rows from the raw_stream.csv file at once.
    """
    return load_stream_rows()