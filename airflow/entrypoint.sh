#!/bin/bash
set -e

echo "🧱 Инициализация БД"
airflow db migrate

echo "👤 Создание пользователя admin (если не существует)"
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

echo "⏳ Ждём загрузки DAG-ов..."
until airflow dags list | grep -q "export_to_yadisk_dag"; do
  echo "DAG-и ещё не найдены, ожидание..."
  sleep 5
done

echo "✅ Разморозка DAG-ов"
airflow dags list | tail -n +2 | awk '{print $1}' | xargs -n1 airflow dags unpause

echo "🎉 Инициализация завершена!"