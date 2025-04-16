# импортируем необходимые модули для работы с Telegram Bot API, моделями, данными и логированием
import os
import requests
import modules.utils as utils
import logging
from aiogram import Bot, types, F, Router
from aiogram.filters import Command
import redis

router = Router()

# обработчик команды /start
@router.message(Command("start"))
async def start_command(message: types.Message, bot: Bot):
    """
    приветствует пользователя
    """
    await utils.log_user_action(message.from_user.id, "start command")
    await message.answer(
            f"*👋 Здравствуйте {message.from_user.full_name} \\!*",
            parse_mode="MarkdownV2"
        )

@router.message(Command("help"))
async def help_command(message: types.Message, bot: Bot):
    """
    показывает список команд
    """
    await utils.log_user_action(message.from_user.id, "help command")

    help_text = (
        "*🛠 Доступные команды:*\n\n"
        "/start — 👋 приветствие и начало работы с ботом\n"
        "/help — ℹ️ показать это справочное сообщение\n"
        "\n"
        "_Просто напиши сообщение — и я отвечу на него с помощью YandexGPT\\._"
    )

    await message.answer(help_text, parse_mode="MarkdownV2")

    

@router.message(F.text)
async def process_message(message: types.Message, bot: Bot):
    """
    генерирует текстовый ответ
    """
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    iam_token = r.get("IAM_TOKEN")
    folder_id = os.getenv("FOLDER_ID")
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt",
        "completionOptions": {"temperature": 0.3, "maxTokens": 1000},
        "messages": [{"role": "user", "text": message.text}],
    }

    URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    response = requests.post(
        URL,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {iam_token}"
        },
        json=data,
    ).json()
    await utils.log_user_action(message.from_user.id, "text message")

    answer = response.get('result', {}).get('alternatives', [{}])[
        0].get('message', {}).get('text', "No answer found.")
    await message.answer(answer, parse_mode="Markdown")
