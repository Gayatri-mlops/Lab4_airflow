# src/load_data.py
import os
import pandas as pd

DATA_PATH = "/opt/airflow/dags/data/churn.csv"

def load_data():
    """Sanity-check the dataset and print shape/columns."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"[load_data] shape={df.shape}")
    print(f"[load_data] columns={list(df.columns)}")
    print(df.head(3))
    return DATA_PATH
