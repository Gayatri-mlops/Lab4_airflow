# src/evaluate_model.py
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix
)

PROC = "/opt/airflow/dags/data/processed_churn.csv"
MODEL_PATH = "/opt/airflow/dags/model/churn_pipeline.joblib"
PRED_PATH = "/opt/airflow/dags/data/predictions.csv"

def evaluate_model():
    """Evaluate the saved pipeline and write predictions.csv"""
    if not os.path.exists(PROC):
        raise FileNotFoundError(f"Missing {PROC}")
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Missing model at {MODEL_PATH}")

    df = pd.read_csv(PROC)
    y = df["Churn"]
    X = df.drop(columns=["Churn"])

    # same split recipe for a fair comparison
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    bundle = joblib.load(MODEL_PATH)
    pipe = bundle["pipeline"]

    y_pred = pipe.predict(X_test)
    y_prob = None
    try:
        y_prob = pipe.predict_proba(X_test)[:, 1]
    except Exception:
        pass

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_prob) if y_prob is not None else None
    cm = confusion_matrix(y_test, y_pred)

    print("\n===== EVAL =====")
    print(f"accuracy  : {acc:.4f}")
    print(f"precision : {prec:.4f}")
    print(f"recall    : {rec:.4f}")
    if roc is not None:
        print(f"roc_auc   : {roc:.4f}")
    print(f"confusion :\n{cm}\n")

    # save predictions
    pd.DataFrame({"actual": y_test.values, "pred": y_pred}).to_csv(PRED_PATH, index=False)
    print(f"[evaluate_model] predictions saved to {PRED_PATH}")

    out = {"accuracy": float(acc), "precision": float(prec), "recall": float(rec)}
    if roc is not None:
        out["roc_auc"] = float(roc)
    return out
