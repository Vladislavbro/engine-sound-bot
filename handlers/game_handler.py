# -*- coding: utf-8 -*-
import random
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

# Импортируем данные, клавиатуры, состояния и утилиты
from data import ENGINES_DATA, ENGINE_TYPES
from keyboards import get_game_keyboard, get_play_again_keyboard
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
            f"Игра окончена! Твой результат: {current_score} из {len(question_list)} угаданных моторов.",
            reply_markup=get_play_again_keyboard()
        )
        await state.clear() # Очищаем состояние
        await state.set_state(None) # Выходим из состояния игры
        return

    # Отправка номера вопроса и счета
    total_questions = len(question_list)
    await bot.send_message(
        chat_id,
        f"Вопрос {question_index + 1} из {total_questions}.\nПравильных ответов: {current_score}"
    )

    # Получаем следующий вопрос (тип мотора)
    correct_answer = question_list[question_index]
    engine_info = ENGINES_DATA[correct_answer]

    # Генерируем варианты ответа
    options = get_random_options(correct_answer, ENGINE_TYPES)

    # Создаем клавиатуру
    keyboard = get_game_keyboard(options, correct_answer)

    # Отправка картинки unknown_car.jpeg
    unknown_car_image = FSInputFile("media/images/unknown_car.jpeg")
    await bot.send_photo(chat_id, photo=unknown_car_image)

    # Отправляем звук
    sound = FSInputFile(engine_info["sound_file"])
    await bot.send_voice(chat_id, voice=sound)

    # Отправляем текст вопроса с клавиатурой
    await bot.send_message(chat_id, "Какой это мотор?", reply_markup=keyboard)

    # Обновляем состояние: номер вопроса и правильный ответ для проверки
    await state.update_data(question_index=question_index + 1, current_correct_answer=correct_answer)
    await state.set_state(GameState.in_game)

# Убрали обработчики start_game_callback_handler и next_question_handler,
# так как они теперь находятся в callback_handler.py 