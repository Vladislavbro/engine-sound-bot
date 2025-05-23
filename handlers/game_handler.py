# -*- coding: utf-8 -*-
import random
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from typing import List

# Импортируем данные, клавиатуры, состояния и утилиты
from data import ENGINES_DATA, ENGINE_TYPES
from keyboards import get_game_keyboard
from states import GameState
from utils import get_random_options

game_router = Router()

async def send_question(chat_id: int, bot: Bot, state: FSMContext):
    """Отправляет следующий вопрос пользователю и сохраняет ID сообщений вопроса."""
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
    unknown_car_image = FSInputFile("media/images/unknown_engine.png")
    sound = FSInputFile(engine_info["sound_file"])

    # --- Отправка сообщений вопроса и сохранение их ID --- H
    msg_ids_to_delete_for_this_q: List[int] = []

    # 1. Картинка unknown_car
    msg1 = await bot.send_photo(chat_id, photo=unknown_car_image)
    msg_ids_to_delete_for_this_q.append(msg1.message_id)

    # 2. Номер вопроса и счет (если не первый вопрос)
    msg2 = None
    question_number_message = f"Вопрос {question_index + 1} из {total_questions}."
    if question_index > 0:
        question_number_message += f"\nПравильных ответов: {current_score}"
    msg2 = await bot.send_message(chat_id, question_number_message)
    msg_ids_to_delete_for_this_q.append(msg2.message_id)

    # 3. Звук мотора (вопроса)
    msg3 = await bot.send_voice(chat_id, voice=sound)
    msg_ids_to_delete_for_this_q.append(msg3.message_id)

    # 4. Текст вопроса и кнопки вариантов (его ID не сохраняем, т.к. удаляется через callback.message)
    await bot.send_message(chat_id, "Какой это мотор?", reply_markup=keyboard)
    # ----------------------------------------------------

    # Обновляем состояние: номер вопроса, правильный ответ и ID сообщений вопроса для удаления
    await state.update_data(
        question_index=question_index + 1,
        current_correct_answer=correct_answer,
        question_msg_ids_to_delete=msg_ids_to_delete_for_this_q
    )
    await state.set_state(GameState.in_game)

# Убрали обработчики start_game_callback_handler и next_question_handler,
# так как они теперь находятся в callback_handler.py 