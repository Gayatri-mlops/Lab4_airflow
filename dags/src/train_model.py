# src/train_model.py
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

PROC = "/opt/airflow/dags/data/processed_churn.csv"
MODEL_DIR = "/opt/airflow/dags/model"
MODEL_PATH = os.path.join(MODEL_DIR, "churn_pipeline.joblib")

def train_model():
    """Fit a robust sklearn Pipeline & persist it."""
    if not os.path.exists(PROC):
        raise FileNotFoundError(f"Missing {PROC}")

    df = pd.read_csv(PROC)
    y = df["Churn"]
    X = df.drop(columns=["Churn"])

    # split with reproducibility
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # auto-detect feature types
    numeric_cols = X_train.select_dtypes(include=["number", "float", "int"]).columns.tolist()
    categorical_cols = [c for c in X_train.columns if c not in numeric_cols]

    numeric_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    pre = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_cols),
            ("cat", categorical_pipe, categorical_cols),
        ]
    )

    clf = LogisticRegression(max_iter=1000, random_state=42)

    pipe = Pipeline(steps=[("pre", pre), ("clf", clf)])

    pipe.fit(X_train, y_train)

    # quick sanity metric on validation
    val_acc = accuracy_score(y_val, pipe.predict(X_val))
    print(f"[train_model] validation accuracy: {val_acc:.4f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({"pipeline": pipe, "numeric_cols": numeric_cols, "categorical_cols": categorical_cols}, MODEL_PATH)
    print(f"[train_model] saved pipeline to {MODEL_PATH}")

    return {"model_path": MODEL_PATH, "val_accuracy": float(val_acc)}
