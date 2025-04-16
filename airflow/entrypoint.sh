#!/bin/bash
set -e

echo "Ожидание PostgreSQL на порту 5432..."
until nc -z postgres 5432; do
  echo "PostgreSQL ещё не доступен, ожидание..."
  sleep 2
done
echo "PostgreSQL доступен"

echo "Инициализация БД"
airflow db migrate

echo "Создание пользователя admin (если не существует)"
if ! airflow users list | grep -q admin; then
  airflow users create \
    --username admin \
    --password admin \
    --firstname Anonymous \
    --lastname X \
    --role Admin \
    --email admin@example.com
else
  echo "Пользователь admin уже существует"
fi

echo "Ожидание загрузки DAG-ов..."
until airflow dags list | grep -q "export_to_yadisk_dag"; do
  echo "DAG-и ещё не найдены, ожидание..."
  sleep 5
done

echo "Разблокировка DAG-ов"
airflow dags list | tail -n +2 | awk '{print $1}' | xargs -n1 airflow dags unpause

echo "Инициализация завершена"