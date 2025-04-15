from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="update_iam_token",
    start_date=datetime(2025, 4, 12),
    schedule_interval="0 * * * *",
    catchup=False,
    tags=["auth", "token"],
) as dag:

    update_token = BashOperator(
        task_id="update_token",
        bash_command="python /opt/airflow/scripts/get_iam_token.py",
        retries=3,
        retry_delay=timedelta(minutes=1)
    )