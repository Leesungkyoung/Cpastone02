import sqlite3
import pandas as pd
import numpy as np
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# --- CONFIG ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "alerts.db"
CSV_PATH = BASE_DIR / "data" / "secom_raw.csv"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize alerts table (reset)."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS alerts")

    cur.execute("""
        CREATE TABLE alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            top_sensors TEXT NOT NULL,
            prob REAL,
            resolved BOOLEAN NOT NULL DEFAULT 0,
            resolved_at TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("🧹 DB 초기화 완료 (alerts 테이블 재생성).")

def seed_data():
    print(f"📌 CSV 불러오는 중: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    # timestamp → datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # product_id는 CSV에서 그대로 가져옴
    if "product_id" not in df.columns:
        print("❌ CSV에 product_id 컬럼이 없음. 다시 생성해주세요.")
        return

    # label = 1 (불량만)
    df_bad = df[df["label"] == 1].copy()
    print(f"📌 불량 데이터 개수: {len(df_bad)}")

    # sensor 칼럼 자동 탐색
    sensor_columns = [c for c in df.columns if c.startswith("sensor_")]

    conn = get_db_connection()
    cur = conn.cursor()

    insert_sql = """
        INSERT INTO alerts (timestamp, product_id, top_sensors, prob, resolved, resolved_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    for _, row in df_bad.iterrows():
        ts = row["timestamp"].isoformat()
        product_id = int(row["product_id"])

        # 더미 top_sensors (랜덤 3개) - 수정된 부분
        top3 = random.sample(sensor_columns, 3)
        top_sensors_json = json.dumps(top3)

        # 임시 예측 확률
        prob = round(0.75 + (0.25 * (hash(ts) % 100) / 100), 4)

        cur.execute(insert_sql, (
            ts,
            product_id,
            top_sensors_json,
            prob,
            0,      # resolved FALSE
            None    # resolved_at
        ))

    conn.commit()
    conn.close()
    print("🎉 Seed Insert 완료! AlertsPage에서 데이터 확인하세요!")

def append_dummy_november_data():
    """Appends 20 synthetic defect data points for November 2008, ensuring they are sequential."""
    print("\n appending 20 sequential synthetic November data points...")
    conn = get_db_connection()
    cur = conn.cursor()

    # Get sensor column names
    try:
        df_temp = pd.read_csv(CSV_PATH, nrows=0)
        sensor_columns = [c for c in df_temp.columns if c.startswith("sensor_")]
    except (FileNotFoundError, IndexError):
        print("Could not read sensor columns from CSV. Using placeholders.")
        sensor_columns = [f"sensor_{i:03d}" for i in range(1, 591)]

    # 1. Generate 20 unique, sorted product IDs between 1 and 500
    product_ids = sorted(random.sample(range(1, 501), 20))

    # 2. Generate 20 sequential timestamps in November 2008
    timestamps = []
    current_time = datetime(2008, 11, 1, 9, 0, 0) # Start date
    for _ in range(20):
        # Add a random interval (e.g., 8 to 36 hours)
        current_time += timedelta(hours=random.randint(8, 36), minutes=random.randint(0, 59))
        timestamps.append(current_time)

    insert_sql = """
        INSERT INTO alerts (timestamp, product_id, top_sensors, prob, resolved, resolved_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    for i in range(20):
        timestamp = timestamps[i].isoformat()
        product_id = product_ids[i]
        
        # Select 3 random sensors
        top_sensors = random.sample(sensor_columns, 3)
        top_sensors_json = json.dumps(top_sensors)
        
        # Generate random probability
        prob = round(random.uniform(0.80, 0.98), 4)

        cur.execute(insert_sql, (
            timestamp,
            product_id,
            top_sensors_json,
            prob,
            0,      # resolved = FALSE
            None    # resolved_at
        ))

    conn.commit()
    conn.close()
    print(f"✅ Successfully appended 20 dummy alerts for November.")


if __name__ == "__main__":
    init_db() # 수정
    seed_data() # 수정
    append_dummy_november_data()