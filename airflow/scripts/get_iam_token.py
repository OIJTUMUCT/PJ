import redis
import requests
import os
from dotenv import load_dotenv

load_dotenv("/opt/airflow/.env")
oauth_token = os.getenv("OAUTH_TOKEN")

r = redis.Redis(host='redis', port=6379, decode_responses=True)

response = requests.post(
    "https://iam.api.cloud.yandex.net/iam/v1/tokens",
    json={"yandexPassportOauthToken": oauth_token}
)

response.raise_for_status()
iam_token = response.json()["iamToken"]

r.set("IAM_TOKEN", iam_token)

print("Новый IAM_TOKEN успешно записан в Redis.")