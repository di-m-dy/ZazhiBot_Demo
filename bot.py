"""
en: The main module of the bot, which runs the bot
ru: Основной модуль бота, который запускает бота
"""

import asyncio
from aiogram import Bot, Dispatcher, types
import logging
from config import BOT_TOKEN
from handlers import admin_handler, user_handler

# en: Configure logging / ru: Настроить логирование
logging.basicConfig(level=logging.INFO)

# en: Initialize bot and dispatcher / ru: Инициализировать бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# en: Include all the handlers / ru: Включить все обработчики
dp.include_router(admin_handler.router)
dp.include_router(user_handler.router)


async def main():
    # en: Set the webhook
    # ru: Установка webhook
    await bot.delete_webhook(drop_pending_updates=True)
    # en: Start the bot
    # ru: Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
