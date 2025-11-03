Project Overview

This project demonstrates an end-to-end Machine Learning workflow orchestrated with Apache Airflow.
The pipeline automates the process of loading, preprocessing, training, and evaluating** a customer churn prediction model — a vital use case for customer retention and business analytics.

---

Project Structure

```bash
airflow_churn_lab/
│
├── dags/
│   └── customer_churn_pipeline.py       # Airflow DAG defining the ML workflow
│
├── src/
│   ├── load_data.py                     # Loads raw churn dataset
│   ├── preprocess_data.py               # Cleans and transforms data for ML
│   ├── train_model.py                   # Trains Logistic Regression model
│   ├── evaluate_model.py                # Evaluates model and logs metrics
│   └── __init__.py
│
├── data/
│   ├── raw_data.csv                     # Original input dataset
│   ├── processed_data.csv               # Preprocessed dataset
│   └── model.pkl                        # Serialized trained model
│
├── docker-compose.yaml                  # Docker setup for Airflow (Scheduler, Webserver, Worker, Postgres, Redis)
├── Dockerfile                           # Custom Airflow image (optional)
├── requirements.txt                     # Python dependencies
└── README.md                            # Project documentation
```

Pipeline Overview

DAG Name: customer_churn_pipeline

This DAG contains four main tasks:

| Task Name         | Description                                                          |
| ----------------- | -------------------------------------------------------------------- |
| `load_data`       | Loads the raw churn dataset into the workflow                        |
| `preprocess_data` | Cleans, encodes, and scales the dataset for model training           |
| `train_model`     | Trains a Logistic Regression model and saves it as `model.pkl`       |
| `evaluate_model`  | Evaluates accuracy, precision, recall, and F1-score, logging results |

**Model Accuracy:** 0.79
**Macro F1-Score:** 0.70
*(Logged in Airflow task logs)*

Key Features

* **Modular Airflow DAG**: Each stage of the ML pipeline is represented as an independent Airflow task.
* **Reproducible Workflow**: Uses Docker Compose to orchestrate Airflow components (webserver, scheduler, worker, Redis, Postgres).
* **Comprehensive Logging**: Evaluation metrics (accuracy, precision, recall, F1-score) logged after each run.
* **Dataset Versioning**: Intermediate data files (raw and processed) saved in `/data/` for reproducibility.
* **Error Handling & Reliability**: Integrated exception handling ensures stable pipeline execution.
* **Containerized Execution**: End-to-end orchestration within isolated Docker containers.
* **Health Verification**: Curl and PowerShell checks used to confirm healthy Airflow services.

Enhancements Implemented

1. **Refactored Source Code** — Split the ML pipeline into modular Python scripts (`load_data.py`, `preprocess_data.py`, `train_model.py`, `evaluate_model.py`).
2. **Improved DAG Reliability** — Added retries, dependencies, and logging configuration.
3. **Added Docker Health Checks** — Ensured that webserver and scheduler containers are healthy before DAG execution.
4. **Integrated Joblib Model Saving** — Serialized models for persistence and later inference.
5. **Enhanced Observability** — Used Airflow task logs to trace each step with metrics and validation reports.
6. **Validated Webserver Health** — Confirmed `http://localhost:8080/health` returned HTTP 200 OK before triggering DAGs.
7. **Full Workflow Verification** — Successfully triggered and completed all DAG tasks (green status).

How to Run

1. Clone the Repository

```bash
git clone <repo_url>
cd airflow_churn_lab
```

2. Start Airflow with Docker

```bash
docker compose up -d
```

Airflow Web UI will be available at:
[http://localhost:8080](http://localhost:8080)

Credentials:

```
Username: admin
Password: admin
```

3. Access Airflow Dashboard

* Go to **[http://localhost:8080/home](http://localhost:8080/home)**
* Find DAG: `customer_churn_pipeline`
* Turn it **ON** using the toggle switch
* Click **Trigger DAG**

Wait a few seconds — task circles will:

* Turn **yellow**  (running)
* Then **green**  (success)

Monitor task progress through **Graph View** or **Logs**.

Technologies Used

* **Apache Airflow** — Workflow orchestration
* **Python 3.9+** — Core programming language
* **scikit-learn** — Machine learning (Logistic Regression)
* **pandas / numpy** — Data cleaning and transformation
* **joblib** — Model serialization
* **Docker & Docker Compose** — Containerized deployment
* **PostgreSQL & Redis** — Airflow backend and queue management

Sample Output (from Logs)

```
Training Accuracy: 0.79
Precision: 0.76
Recall: 0.72
Macro F1-Score: 0.70
Model saved successfully as model.pkl
```
Screenshots

Include screenshots here, for example:

* DAG view (`customer_churn_pipeline`)
* Graph view showing all green tasks
* Airflow Web UI running at `http://localhost:8080/home`
Screenshots from the successful execution of the customer_churn_pipeline DAG are included in the Results/ folder.


