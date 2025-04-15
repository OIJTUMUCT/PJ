import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from modules.handlers import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# создаём бота с токеном из переменной окружения
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

# основная асинхронная функция, запускающая бота
async def main():
    try:
        logger.info(">>> BOT STARTED")
        dp.include_router(router)
        logger.info(">>> Router included")
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Ошибка запуска бота: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Бот завершился с ошибкой: {e}")
        sys.exit(1)