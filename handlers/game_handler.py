# -*- coding: utf-8 -*-
import random
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

# Импортируем данные, клавиатуры, состояния и утилиты
from data import ENGINES_DATA, ENGINE_TYPES
from keyboards import get_game_keyboard, get_play_again_keyboard # get_next_keyboard пока не нужен
from states import GameState
from utils import get_random_options

game_router = Router() # Создаем роутер для этого хэндлера

async def send_question(chat_id: int, bot: Bot, state: FSMContext):
    """Отправляет следующий вопрос пользователю."""
    user_data = await state.get_data()
    question_list = user_data.get('questions', [])
    current_score = user_data.get('score', 0)
    question_index = user_data.get('question_index', 0)

    if question_index >= len(question_list):
        # Игра окончена
        await bot.send_message(
            chat_id,
            f"Игра окончена! Ты угадал {current_score} из {len(question_list)} типов моторов.",
            reply_markup=get_play_again_keyboard()
        )
        await state.clear() # Очищаем состояние
        return

    # Получаем следующий вопрос (тип мотора)
    correct_answer = question_list[question_index]
    engine_info = ENGINES_DATA[correct_answer]

    # Генерируем варианты ответа
    options = get_random_options(correct_answer, ENGINE_TYPES)

    # Создаем клавиатуру
    keyboard = get_game_keyboard(options, correct_answer)

    # Отправляем звук
    sound = FSInputFile(engine_info["sound_file"])
    await bot.send_voice(chat_id, voice=sound)

    # Отправляем вопрос с клавиатурой
    await bot.send_message(chat_id, "Какой это мотор?", reply_markup=keyboard)

    # Обновляем состояние: номер вопроса и правильный ответ для проверки
    await state.update_data(question_index=question_index + 1, current_correct_answer=correct_answer)
    await state.set_state(GameState.in_game)


# Обработчик нажатия кнопки "Начать" (callback_data="start_game")
@game_router.callback_query(F.data == "start_game")
async def start_game_callback_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Начинает игру при нажатии кнопки 'Начать'."""
    await callback.answer() # Отвечаем на колбэк
    if callback.message:
        await callback.message.edit_reply_markup() # Убираем кнопку "Начать"

    # Перемешиваем типы моторов для нового раунда
    shuffled_engines = random.sample(ENGINE_TYPES, len(ENGINE_TYPES))

    # Сохраняем список вопросов и начальный счет в состояние
    await state.update_data(questions=shuffled_engines, score=0, question_index=0)

    # Отправляем первый вопрос
    if callback.message:
        await send_question(callback.message.chat.id, bot, state)

# TODO: Добавить обработчик нажатия кнопки "Дальше"
# @game_router.message(F.text == "Дальше") # Или использовать CallbackQuery
async def next_question_handler(message: Message, state: FSMContext):
    """Отправляет следующий вопрос."""
    # Логика отправки следующего вопроса
    pass 