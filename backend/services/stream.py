# backend/services/stream.py

import csv
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STREAM_FILE_PATH = DATA_DIR / "raw_stream.csv"

def load_stream_rows():
    """
    Loads and sorts all rows from the raw_stream.csv file.
    """
    try:
        with open(STREAM_FILE_PATH, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            rows = [row for row in reader]
        
        rows.sort(key=lambda x: int(x['product_id']))
        return rows
    except FileNotFoundError:
        print(f"Error: Stream data file not found at {STREAM_FILE_PATH}")
        return []
    except Exception as e:
        print(f"An error occurred while loading stream data: {e}")
        return []