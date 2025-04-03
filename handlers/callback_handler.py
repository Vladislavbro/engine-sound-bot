# -*- coding: utf-8 -*-
import random
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.enums import ParseMode

# Импортируем данные, клавиатуры, состояния
from data import ENGINES_DATA, ENGINE_TYPES
from keyboards import get_play_again_keyboard # Восстановлен импорт
from states import GameState
# Импортируем функцию отправки вопроса
from handlers.game_handler import send_question
# Убраны импорты из start_handler

callback_router = Router()

@callback_router.callback_query(F.data.startswith("answer:"), GameState.in_game)
async def process_answer_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Обрабатывает ответ, показывает результат и сразу отправляет след. вопрос/финал."""
    await callback.answer()
    _, selected_option, correct_answer_key = callback.data.split(":")
    user_data = await state.get_data()
    current_score = user_data.get('score', 0)
    question_index = user_data.get('question_index', 0)
    question_list = user_data.get('questions', [])
    total_questions = len(question_list)
    engine_info = ENGINES_DATA[correct_answer_key]
    image = FSInputFile(engine_info["image_file"])
    correct_sound = FSInputFile(engine_info["sound_file"])
    display_name = engine_info.get("display_name", correct_answer_key)
    car_name = engine_info.get("car", "")
    result_message = ""
    if selected_option == correct_answer_key:
        result_message = f"✅ Правильно! Это {display_name} {car_name}."
        current_score += 1
        await state.update_data(score=current_score)
    else:
        result_message = f"❌ Неправильно. Это был {display_name} {car_name}."
    
    chat_id = callback.message.chat.id
    if callback.message:
        try:
            await callback.message.delete()
        except (TelegramBadRequest, TelegramForbiddenError) as e:
            print(f"Error deleting callback message: {e}")

    await bot.send_message(chat_id, result_message)
    await bot.send_photo(chat_id, photo=image)
    await bot.send_voice(chat_id, voice=correct_sound)

    # Проверка на последний вопрос
    if question_index >= total_questions:
        final_text = ""
        final_image_path = ""
        # (if/elif/else для счета)
        if 0 <= current_score <= 4:
            final_image_path = "media/images/lada.jpeg"
            final_text = (f"Ты набрал {current_score} из {total_questions}. Спасибо за игру! "
                          f"В нашей игре никто не уходит без приза, поэтому мы дарим тебе заряженную двенашку. "
                          f"А если хочешь знать о машинах больше — подисывайся на мой канал @poooweeeer.")
        elif 5 <= current_score <= 7:
            final_image_path = "media/images/miata.jpeg"
            final_text = (f"Ты набрал {current_score} из {total_questions}. Похоже, ты разбираешься в автомобилях! "
                          f"В нашей игре никто не уходит без приза, мы дарим тебе машину, которую выбирают только те, кто шарит."
                          f"А если хочешь знать о машинах больше — подисывайся на мой канал @poooweeeer.")
        elif current_score == 8: # Perfect score
            final_image_path = "media/images/daytona.jpeg"
            final_text = (f"Ты набрал {current_score} из {total_questions}! Браво, ты настоящая легенда автомобильного мира! "
                          f"Ты достоин машины, которую поймут только ценители, Daytona SP3 твоя."
                          f"А если хочешь знать о машинах еще больше — подисывайся на мой канал @poooweeeer.")
        else: 
            final_text = f"Игра окончена! Твой результат: {current_score} из {total_questions} угаданных моторов."
        
        if final_image_path:
            try:
                final_image = FSInputFile(final_image_path)
                await bot.send_photo(chat_id, photo=final_image)
            except Exception as e:
                print(f"Error sending final image {final_image_path}: {e}")
                final_text = f"Игра окончена! Твой результат: {current_score} из {total_questions} угаданных моторов."

        # --- Отправляем финальный текст С КНОПКАМИ "Сыграть еще" / "Завершить" --- H
        await bot.send_message(
            chat_id,
            final_text,
            reply_markup=get_play_again_keyboard() # Возвращаем клавиатуру
        )
        await state.clear() # Очищаем состояние ПОСЛЕ показа результата
        await state.set_state(None)
    else:
        # Сразу отправляем следующий вопрос
        await send_question(chat_id, bot, state)

# Обработчик ТОЛЬКО для САМОЙ ПЕРВОЙ кнопки "Начать"
@callback_router.callback_query(F.data == "start_game")
async def start_game_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Начинает игру при нажатии самой первой кнопки 'Начать'."""
    await callback.answer()
    chat_id = callback.message.chat.id

    # --- Заменяем удаление на редактирование (убираем кнопку) --- H
    if callback.message:
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except (TelegramBadRequest, TelegramForbiddenError) as e:
            print(f"Could not edit start_game button message: {e}")
    # ------------------------------------------------------------

    # Инициализируем состояние для НОВОЙ игры
    await state.set_data({
        'questions': random.sample(ENGINE_TYPES, len(ENGINE_TYPES)),
        'score': 0,
        'question_index': 0,
    })

    # Отправляем первый вопрос
    await send_question(chat_id, bot, state)

# --- Обработчик для кнопки "Сыграть ещё" --- H
@callback_router.callback_query(F.data == "play_again")
# Добавляем bot в параметры
async def play_again_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Показывает инструкцию по перезапуску игры в новом сообщении."""
    await callback.answer()
    # --- Изменен текст инструкции --- H
    instruction_text = ("Чтобы сыграть еще раз очисти историю этого чата "
                        "(в меню чата выбери 'Очистить историю') и нажми 'Начать' в первом сообщении.")
    if callback.message:
        chat_id = callback.message.chat.id # Получаем chat_id
        # --- Отправляем инструкцию НОВЫМ сообщением --- H
        try:
            await bot.send_message(chat_id, instruction_text)
            # --- Убираем кнопки из предыдущего сообщения (с результатами) --- H
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except (TelegramBadRequest, TelegramForbiddenError) as e_edit:
                print(f"Could not edit reply markup for play_again message: {e_edit}")
            # ------------------------------------------------------------------
        except Exception as e:
            print(f"Could not send instruction message for play_again: {e}")
            # Если не удалось отправить инструкцию, хотя бы уберем кнопки
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception as e_edit_fallback:
                 print(f"Could not edit reply markup (fallback) for play_again: {e_edit_fallback}")
        # -------------------------------------------------------

    await state.clear() # Очищаем состояние в любом случае

# Обработчик кнопки "Завершить"
@callback_router.callback_query(F.data == "quit_game")
async def quit_game_callback_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Завершает игру и очищает состояние, НЕ удаляя сообщения игры."""
    await callback.answer()
    # chat_id = callback.message.chat.id # chat_id не нужен здесь

    # Редактируем сообщение с кнопкой "Завершить" на прощальное
    if callback.message:
        try:
            await callback.message.edit_text("Спасибо за игру! 👋\nНадеюсь, тебе понравилось. До скорого!", parse_mode=ParseMode.HTML)
        except (TelegramBadRequest, TelegramForbiddenError) as e:
             print(f"Could not edit quit_game message: {e}")
             # Если редактирование не удалось, ничего страшного

    await state.clear() # Очищаем состояние в самом конце 