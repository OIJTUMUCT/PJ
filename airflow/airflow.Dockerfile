FROM apache/airflow:2.7.3-python3.11

USER airflow
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

USER root
COPY ./entrypoint.sh /opt/airflow/scripts/entrypoint.sh
RUN chmod +x /opt/airflow/scripts/entrypoint.sh

USER airflow