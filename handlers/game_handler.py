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
    total_questions = len(question_list)

    # Код для завершения игры (если вопросы кончились) остается на всякий случай,
    # но по новой логике мы должны попасть сюда только если что-то пошло не так.
    if question_index >= total_questions:
        await bot.send_message(
            chat_id,
            f"Игра окончена! Твой результат: {current_score} из {total_questions} угаданных моторов.",
            reply_markup=get_play_again_keyboard()
        )
        await state.clear()
        await state.set_state(None)
        return

    # Получаем данные для текущего вопроса
    correct_answer = question_list[question_index]
    engine_info = ENGINES_DATA[correct_answer]
    options = get_random_options(correct_answer, ENGINE_TYPES)
    keyboard = get_game_keyboard(options, correct_answer)
    unknown_car_image = FSInputFile("media/images/unknown_car.png")
    sound = FSInputFile(engine_info["sound_file"])

    # --- Измененный порядок отправки --- H
    # 1. Картинка unknown_car
    await bot.send_photo(chat_id, photo=unknown_car_image)

    # 2. Номер вопроса и счет (если не первый вопрос)
    question_number_message = f"Вопрос {question_index + 1} из {total_questions}."
    if question_index > 0: # Не показываем счет на первом вопросе
        question_number_message += f"\nПравильных ответов: {current_score}"
    await bot.send_message(chat_id, question_number_message)

    # 3. Звук мотора
    await bot.send_voice(chat_id, voice=sound)

    # 4. Текст вопроса и кнопки вариантов
    await bot.send_message(chat_id, "Какой это мотор?", reply_markup=keyboard)
    # -----------------------------------

    # Обновляем состояние: номер вопроса для следующего шага и правильный ответ для проверки
    await state.update_data(question_index=question_index + 1, current_correct_answer=correct_answer)
    await state.set_state(GameState.in_game)

# Убрали обработчики start_game_callback_handler и next_question_handler,
# так как они теперь находятся в callback_handler.py 