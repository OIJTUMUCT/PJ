from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="init_postgres_schema",
    start_date=datetime(2025, 4, 12),
    schedule="@once",
    catchup=False,
    tags=["init", "postgres"],
) as dag:

    init_db = BashOperator(
        task_id="init_user_actions_table",
        bash_command="python /opt/airflow/scripts/init_db.py",
        retries=3,
        retry_delay=timedelta(minutes=1)
    )