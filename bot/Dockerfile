FROM python:3.11-slim

# Установим переменные окружения для безопасного запуска
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Установка зависимостей системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только requirements.txt, чтобы не кэшировать старый код
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код уже после установки зависимостей
COPY . .

CMD ["python", "main.py"]

