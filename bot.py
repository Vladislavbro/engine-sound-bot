# -*- coding: utf-8 -*-
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
# Импортируем роутеры из хэндлеров
from handlers.start_handler import start_router
from handlers.game_handler import game_router
from handlers.callback_handler import callback_router
# --- Добавлено: Импорт инициализации БД --- H
from database import init_db

async def main() -> None:
    # Используем MemoryStorage для хранения состояний FSM в памяти
    # Для продакшена лучше использовать RedisStorage или другое персистентное хранилище
    storage = MemoryStorage()

    # Инициализация бота и диспетчера
    # Задаем настройки по умолчанию через DefaultBotProperties
    default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=BOT_TOKEN, default=default_properties)
    dp = Dispatcher(storage=storage)

    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(game_router)
    dp.include_router(callback_router)

    # --- Добавлено: Инициализация БД перед запуском --- H
    init_db()
    # ----------------------------------------------

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) 