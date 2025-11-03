# src/preprocess_data.py
import os
import pandas as pd

RAW = "/opt/airflow/dags/data/churn.csv"
PROC = "/opt/airflow/dags/data/processed_churn.csv"

def preprocess_data():
    """Clean dataset & encode target, save processed CSV."""
    if not os.path.exists(RAW):
        raise FileNotFoundError(f"Missing {RAW}")

    df = pd.read_csv(RAW)

    # Drop obvious ID column if present
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])

    # Fix TotalCharges which often has spaces/empty strings
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Drop any rows missing the target or numeric conversion failures
    if "Churn" not in df.columns:
        raise ValueError("Expected 'Churn' column not found.")
    df = df.dropna(subset=["Churn", "TotalCharges"])

    # Encode target
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0}).astype(int)

    # Save
    df.to_csv(PROC, index=False)
    print(f"[preprocess_data] saved {PROC} with shape={df.shape}")
    return PROC
