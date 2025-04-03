# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# TODO: Импортировать данные, клавиатуры, состояния
# from data import ENGINES_DATA, ENGINE_TYPES
# from keyboards import get_game_keyboard, get_next_keyboard
# from states import GameState
# from utils import get_random_options

game_router = Router() # Создаем роутер для этого хэндлера

# TODO: Добавить обработчик нажатия кнопки "Начать"
# @game_router.message(F.text == "Начать") # Или использовать CallbackQuery, если кнопка инлайн
async def start_game_handler(message: Message, state: FSMContext):
    """Начинает игру или отправляет следующий вопрос."""
    # Логика начала игры: перемешать вопросы, установить состояние, отправить первый вопрос
    pass

# TODO: Добавить обработчик нажатия кнопки "Дальше"
# @game_router.message(F.text == "Дальше") # Или использовать CallbackQuery
async def next_question_handler(message: Message, state: FSMContext):
    """Отправляет следующий вопрос."""
    # Логика отправки следующего вопроса
    pass 