# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

# TODO: Импортировать необходимые данные, клавиатуры, состояния
# from data import ENGINES_DATA
# from keyboards import get_next_keyboard
# from states import GameState

callback_router = Router() # Создаем роутер для этого хэндлера

# TODO: Добавить обработчик колбэков с ответами
# @callback_router.callback_query(GameState.waiting_for_answer) # Пример
async def process_answer_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает ответ пользователя."""
    # Логика проверки ответа, отправки результата, звука, картинки и кнопки "Дальше"
    await callback.answer() # Отвечаем на колбэк, чтобы убрать "часики"
    pass

# TODO: Добавить обработчик колбэка "Сыграть еще"
async def play_again_callback(callback: CallbackQuery, state: FSMContext):
    """Начинает новую игру после завершения предыдущей."""
    # Сбросить состояние, начать новую игру
    await callback.answer()
    pass 