# Структура проекта

![image](https://github.com/user-attachments/assets/45dd4a68-094d-45e3-98d8-ea3ac44809f3)

Deploy----------------------------------------------------------------
        ┌──────────────┐   ┌──────────────┐
        |GitHub Actions|   │GitHub Secrets│     
        └────────────┬─┘   └─┬────────────┘
                     |       |
                     |       |
                ┌────▼──────┐|
                │  Ansible  │|
                └────┬──────┘|
                     |       |
                     |  ┌────▼───────┐
                     |  │   .env     │
                     |  └────┬───────┘
Work-----------------|-------│----------------------------------------
             ┌───────▼───────▼─────────────┐
             │       docker-compose        │
             └────┬───────────────┬────────┘
                  │               │
       ┌──────────▼──┐      ┌─────▼────────┐     API YANDEX GPT   
       │  postgres   │◄────►│ telegram-bot │◄─────────────────────►
       └────┬─────┬──┘      └─────▼────────┘        DataLens
            │     └────────►─────┐│┌────┬───►─────────────────────►
      ┌─────▼────────────┐       └─┘    │
      │ airflow-init     │        │     │
      └─────┬────────────┘        │     │
      ┌─────▼────────────┐        │     │
      │ airflow-webserver│        │     │
      └─────┬────────────┘        │     │
      ┌─────▼────────────┐        │     │
 ┌───►│ airflow-scheduler│        │     │
 |    └─────┬────────────┘        │     │
 |          │ UPDATE AIM_TOKEN    │     │
 |     ┌────▼────┐                │     │
 |     │  redis  │◄───────────────┘     │
 |     └─────────┘     AIM_TOKEN        │
 |                                      │
 |                                      │
 └───►API YANDEX DISK►──────────────────┘

### 🔧 Сервисы:
#### postgres
-- База данных

- Образ: postgres:15
- Открытый порт: 5432
- Переменные окружения:
POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB — из .env
- Тома:
pg_data — для хранения данных
postgres.conf и pg_hba.conf — кастомные конфиги для хоста БД
Поведение при падении: restart: always

#### redis
-- Кеш

- Образ: redis:7
- Открытый порт: 6379
- Автоперезапуск: always

#### telegram-bot
-- Пользовательский бот, обменивающийся данными с PostgreSQL/Redis

- Собирается из: ./bot/
- Использует .env
- Зависимости: postgres, redis
- Автоперезапуск: always

#### airflow-init
-- Одноразовая инициализация Airflow:

- Миграция БД
- Создание admin-пользователя
- Разблокировка DAG-ов
- Dockerfile: ./airflow/airflow.Dockerfile
- Точка входа: entrypoint.sh
- Подключения: к БД PostgreSQL
- Монтируемые директории:
DAG-и → /opt/airflow/dags
Скрипты → /opt/airflow/scripts
.env → внутрь контейнера
- Зависит от: postgres

#### airflow-webserver
-- UI интерфейс Airflow

- Порт: 8080
- Команда: webserver
- Монтирует те же папки, что и init
- Зависит от: airflow-init

#### airflow-scheduler
-- Планировщик задач Airflow

- Команда: scheduler
- Те же монтирования и переменные
- Зависит от: airflow-init
