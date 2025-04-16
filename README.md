## 🔍 Информация для проверки
![image](https://github.com/user-attachments/assets/af0e98cc-50e5-4ea4-a823-509ebb3ac836)
- 🤖 Telegram-бот: [`@buchatti_bot`](https://t.me/buchatti_bot)
- 📁 [Папка на Яндекс.Диске (.xlsx)](https://disk.yandex.ru/d/5Ac0VTz1wtP_ow)
- 📊 [Дашборд (источник — Яндекс.Диск)](https://datalens.yandex/9iiwr4valmgav)
- 🧮 [Дашборд (источник — PostgreSQL)](https://datalens.yandex/z8fj31p2tf5el)

#### Навигация по проекту:
- bot/modules содержит в себе:
  - скрипт, описывающий функционал работы бота 'handlers.py'
  - скрипт для взаимодействия бота с PostgreSQL
- airflow/ содержит в себе:
  - dags/ dag-файлы для отработки скриптов по расписанию
  - scripts/ скрипт для инициализации БД 'init_db.py', получения AIM_TOKEN 'get_iam_token.py', экспорта файла на Яндекс.Диск 'export_csv_to_yadisk' (старое название - экспортирует НЕ .csv, а .xlsx)
  - entrypoint.sh для инициализации airflow и разблокировки (включения) dags
- postgres/conf содержит корректировочные конфиги для открытия доступа к PostgreSQL-серверу 
- docker-compose.yml конфиги оркестратора контейнеров
- .github/workflows/deploy.yaml GitHub Actions (AC/ID-скрипт управления деплоем)
- prepare-vm.yml конфиги ansible (часть деплоя -  позволяет автоматически установить Docker и Docker Compose, а также выполнить необходимые настройки)
## Структура проекта

![image](https://github.com/user-attachments/assets/319759c7-f830-4d31-87ce-a2169eda0614)

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
