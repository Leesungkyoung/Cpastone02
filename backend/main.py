
# 수정
# To run this API server, execute the following command from the project root (capstone02_project/):
# uvicorn backend.main:app --reload

import warnings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
import sys

# Add backend directory to sys.path
# This is a common pattern for structuring FastAPI projects
# to ensure consistent module resolution.
# ... (sys.path logic)

from .database import engine, Base
from .routers import predict, stream, alerts, reports, settings

# Create database tables
Base.metadata.create_all(bind=engine)


# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')
warnings.filterwarnings("ignore", category=FutureWarning, module='sklearn')
warnings.filterwarnings("ignore", category=UserWarning, module='joblib')
try:
    from pandas.errors import PerformanceWarning
    warnings.filterwarnings("ignore", category=PerformanceWarning)
except ImportError:
    pass


app = FastAPI(
    title="ZeroQ Factory Monitoring API",
    description="API for real-time monitoring of manufacturing processes.",
    version="1.0.0",
)

# CORS Middleware setup
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api")
app.include_router(stream.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(settings.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    pass

@app.get("/")
def read_root():
    return {"message": "Welcome to ZeroQ Factory Monitoring API"}