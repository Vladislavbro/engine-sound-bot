# -*- coding: utf-8 -*-
from aiogram import Router, F # Добавили F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode

from keyboards import get_start_keyboard # Импортируем клавиатуру

start_router = Router() # Создаем роутер для этого хэндлера

START_MESSAGE = (
    f"Привет! 👋 Это игра <b>'Угадай мотор по звуку'</b>.\n\n"
    f"<b>Правила такие:</b>\n"
    f"1. Я пришлю звук мотора.\n"
    f"2. Ты выбираешь один из 4 предложенных вариантов ответа.\n"
    f"3. Всего будет 8 вопросов, по одному на каждый уникальный тип мотора.\n"
    f"4. В конце считаем насколько ты хорош в угадывании моторов.\n\n"
    f"Удачи!  Нажми 'Начать', чтобы проверить свои знания!"
)

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    keyboard = get_start_keyboard()
    await message.answer(START_MESSAGE, reply_markup=keyboard)

# Обработчик для текстовых сообщений, похожих на старт
@start_router.message(F.text.lower().contains(["старт", "привет", "игра", "начать", "поехали", "го", "давай"]))
async def text_start_handler(message: Message) -> None:
    """Обрабатывает текстовые сообщения, предлагая начать игру."""
    keyboard = get_start_keyboard()
    await message.reply(
        f"""Привет, {hbold(message.from_user.full_name)}! Хочешь сыграть в 'Угадай мотор по звуку'?
{START_MESSAGE}""",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    ) 