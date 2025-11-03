# dags/churn_dag.py
from airflow.decorators import dag, task
from datetime import datetime
from src.load_data import load_data
from src.preprocess_data import preprocess_data
from src.train_model import train_model
from src.evaluate_model import evaluate_model

@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={"owner": "airflow", "retries": 0},
    description="Customer churn classification (TaskFlow, sklearn Pipeline)",
    tags=["mlops", "churn", "sklearn"],
)
def customer_churn_pipeline():
    @task
    def t_load():
        # Just logs and sanity checks; returns path for visibility
        return load_data()

    @task
    def t_preprocess():
        # Cleans data and writes processed_churn.csv
        return preprocess_data()

    @task
    def t_train():
        # Trains sklearn Pipeline (ColumnTransformer+LogReg), saves joblib
        # returns dict with paths + basic metrics from training split
        return train_model()

    @task
    def t_eval():
        # Loads model and evaluates on a held-out split; writes predictions.csv
        return evaluate_model()

    # Order: load -> preprocess -> train -> evaluate
    t_load() >> t_preprocess() >> t_train() >> t_eval()

dag = customer_churn_pipeline()
