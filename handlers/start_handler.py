# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from keyboards import get_start_keyboard # Импортируем клавиатуру

start_router = Router() # Создаем роутер для этого хэндлера

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    keyboard = get_start_keyboard() # Получаем клавиатуру
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}! Угадай тип мотора по звуку. "
        f"Я пришлю тебе звук, а ты выбери правильный из 4 вариантов. Всего 8 вопросов — " # Обновлено на 8 вопросов
        f"по одному на каждый тип мотора. Нажми 'Начать'!",
        reply_markup=keyboard # Добавляем клавиатуру к сообщению
    ) 