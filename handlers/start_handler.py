# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# TODO: Импортировать клавиатуру для старта
# from keyboards import get_start_keyboard

start_router = Router() # Создаем роутер для этого хэндлера

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    # TODO: Добавить клавиатуру к приветственному сообщению
    # keyboard = get_start_keyboard()
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}! Угадай тип мотора по звуку. "
        f"Я пришлю тебе звук, а ты выбери правильный из 4 вариантов. Всего 10 вопросов — "
        f"по одному на каждый тип мотора. Нажми 'Начать'!",
        # reply_markup=keyboard
    ) 