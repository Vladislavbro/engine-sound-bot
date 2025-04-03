# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode

from keyboards import get_start_keyboard

start_router = Router() # Создаем роутер для этого хэндлера

START_MESSAGE = (
    f"Привет! 👋 Это игра <b>'Угадай мотор по звуку'</b>.\n\n"
    f"<b>Правила:</b>\n"
    f"1. Я пришлю звук мотора.\n"
    f"2. Ты выбираешь один из 4 предложенных вариантов ответа.\n"
    f"3. Всего будет 8 вопросов, по одному на каждый уникальный тип мотора.\n"
    f"4. В конце считаем сколько правильных ответов.\n"
    f"5. Бонус: все машины остануться в чате, чтобы ты всегда мог их послушать.\n\n"
    f"Удачи!  Нажми 'Начать', и покажи всем кто тут легенда автомбильного мира!"
)

COVER_IMAGE_PATH = "media/images/cover.png" # Путь к обложке

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    keyboard = get_start_keyboard()
    cover_image = FSInputFile(COVER_IMAGE_PATH)
    # Сначала отправляем обложку
    await message.answer_photo(photo=cover_image)
    # Потом текст с правилами и кнопкой
    await message.answer(START_MESSAGE, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# Обработчик для текстовых сообщений, похожих на старт
@start_router.message(F.text.lower().contains(["старт", "привет", "игра", "начать", "поехали", "го", "давай"]))
async def text_start_handler(message: Message) -> None:
    """Обрабатывает текстовые сообщения, предлагая начать игру."""
    keyboard = get_start_keyboard()
    cover_image = FSInputFile(COVER_IMAGE_PATH)
    # Сначала отправляем обложку (через reply_photo)
    await message.reply_photo(photo=cover_image)
    # Потом текст с правилами и кнопкой (через reply)
    await message.reply(
        f"""Привет, {hbold(message.from_user.full_name)}! Хочешь сыграть в 'Угадай мотор по звуку'?
{START_MESSAGE}""",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    ) 