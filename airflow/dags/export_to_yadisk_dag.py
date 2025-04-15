from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime
from datetime import timedelta
import asyncio

from scripts.export_csv_to_yadisk import fetch_user_actions, convert_to_xlsx_memory, upload_to_yandex

def export_and_upload():
    rows = asyncio.run(fetch_user_actions())
    xlsx_memory = convert_to_xlsx_memory(rows)
    upload_to_yandex(xlsx_memory)

with DAG(
    dag_id="export_user_actions_to_yadisk",
    start_date=datetime(2025, 4, 13),
    schedule_interval="*/5 * * * *",
    catchup=False,
    tags=["export", "yadisk"],
) as dag:

    task = PythonOperator(
        task_id="export_and_upload",
        python_callable=export_and_upload,
        retries=3,
        retry_delay=timedelta(minutes=1),
    )