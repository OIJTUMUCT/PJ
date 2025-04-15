import os
import io
import requests
import asyncpg
import asyncio
import pandas as pd
from urllib.parse import quote


FILENAME = f"user_actions_latest.xlsx"
FOLDER_NAME = "exports"
DISK_PATH = f"{FOLDER_NAME}/{FILENAME}"

OAUTH_TOKEN = os.getenv("OAUTH_YANDEX_DISK_TOKEN")
HEADERS = {"Authorization": f"OAuth {OAUTH_TOKEN}"}


async def fetch_user_actions():
    conn = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    rows = await conn.fetch("SELECT * FROM user_actions")
    await conn.close()
    return rows


def convert_to_xlsx_memory(rows):
    df = pd.DataFrame(rows, columns=["id", "user_id", "action", "timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="User Actions")
    buffer.seek(0)
    return buffer


def ensure_folder_exists(folder):
    encoded_path = quote(folder)
    check = requests.get(
        "https://cloud-api.yandex.net/v1/disk/resources",
        headers=HEADERS,
        params={"path": encoded_path}
    )
    if check.status_code == 200:
        print(f"Папка '{folder}' уже существует.")
    elif check.status_code == 404:
        print(f"Папка '{folder}' не найдена, создаю...")
        create = requests.put(
            "https://cloud-api.yandex.net/v1/disk/resources",
            headers=HEADERS,
            params={"path": encoded_path}
        )
        if create.status_code == 201:
            print(f"Папка '{folder}' успешно создана.")
        else:
            print(f"Ошибка создания папки: {create.status_code} — {create.text}")
    else:
        print(f"Ошибка при проверке папки: {check.status_code} — {check.text}")


def upload_to_yandex(xlsx_memory: io.BytesIO):
    ensure_folder_exists(FOLDER_NAME)

    encoded_file_path = quote(DISK_PATH)
    response = requests.get(
        "https://cloud-api.yandex.net/v1/disk/resources/upload",
        headers=HEADERS,
        params={"path": encoded_file_path, "overwrite": "true"}
    )

    upload_url = response.json().get("href")
    if not upload_url:
        print("Не удалось получить URL загрузки:", response.text)
        return

    upload_resp = requests.put(upload_url, data=xlsx_memory.getvalue())
    if upload_resp.status_code == 201:
        print(f"Успешно загружено: {DISK_PATH}")
    else:
        print(f"Ошибка загрузки: {upload_resp.status_code} — {upload_resp.text}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    rows = loop.run_until_complete(fetch_user_actions())
    xlsx_memory = convert_to_xlsx_memory(rows)
    upload_to_yandex(xlsx_memory)