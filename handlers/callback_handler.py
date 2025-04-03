# -*- coding: utf-8 -*-
import random # Добавили импорт random
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ParseMode # Добавил ParseMode для HTML в quit_game

# TODO: Импортировать необходимые данные, клавиатуры, состояния
# from data import ENGINES_DATA
# from keyboards import get_next_keyboard
# from states import GameState

# Импортируем необходимые данные, клавиатуры, состояния
from data import ENGINES_DATA, ENGINE_TYPES # Добавили ENGINE_TYPES
from keyboards import get_play_again_keyboard # Убрали get_next_keyboard
from states import GameState
# Импортируем функцию отправки вопроса
from handlers.game_handler import send_question

callback_router = Router() # Создаем роутер для этого хэндлера

# Обработчик колбэков с ответами (срабатывает в состоянии in_game)
@callback_router.callback_query(F.data.startswith("answer:"), GameState.in_game)
async def process_answer_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Обрабатывает ответ, удаляет сообщения вопроса, показывает результат и сразу отправляет следующий вопрос."""
    await callback.answer() # Отвечаем на колбэк

    # Извлекаем данные из callback_data
    # Формат: "answer:выбранный_ответ:правильный_ответ"
    _, selected_option, correct_answer_key = callback.data.split(":") # Переименовали в key

    user_data = await state.get_data()
    current_score = user_data.get('score', 0)
    question_index = user_data.get('question_index', 0)
    question_list = user_data.get('questions', [])
    total_questions = len(question_list)
    # Получаем ID сообщений вопроса для удаления
    message_ids_to_delete = user_data.get('question_message_ids', [])

    # Получаем всю информацию о правильном моторе
    engine_info = ENGINES_DATA[correct_answer_key]
    image = FSInputFile(engine_info["image_file"])
    # --- Добавлено: Получаем путь к правильному звуку --- H
    correct_sound = FSInputFile(engine_info["sound_file"])
    # ----------------------------------------------------
    # --- Получаем нужные строки для сообщения --- H
    display_name = engine_info.get("display_name", correct_answer_key) # Отображаемое имя мотора
    car_name = engine_info.get("car", "") # Название машины
    # -----------------------------------------
    result_message = ""

    if selected_option == correct_answer_key: # Используем key
        # --- Формируем новое сообщение (правильно) --- H
        result_message = f"✅ Правильно! Это {display_name} {car_name}."
        current_score += 1
        await state.update_data(score=current_score)
    else:
        # --- Формируем новое сообщение (неправильно) --- H
        result_message = f"❌ Неправильно. Это был {display_name} {car_name}."

    # Удаление сообщений вопроса
    if callback.message:
        chat_id = callback.message.chat.id # Сохраняем chat_id перед удалением
        try:
            await callback.message.delete()
        except TelegramBadRequest as e:
            print(f"Error deleting callback message: {e}")
        for msg_id in message_ids_to_delete:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except TelegramBadRequest as e:
                # Сообщение могло быть уже удалено, или что-то пошло не так, игнорируем
                print(f"Error deleting message {msg_id}: {e}")

        # Отправляем результат, картинку и ПРАВИЛЬНЫЙ ЗВУК
        await bot.send_message(chat_id, result_message)
        await bot.send_photo(chat_id, photo=image)
        await bot.send_voice(chat_id, voice=correct_sound)

        # Проверка на последний вопрос
        if question_index >= total_questions:
            # Показываем финальный результат
            await bot.send_message(
                chat_id,
                f"\n\nИгра окончена! Твой результат: {current_score} из {total_questions} угаданных моторов.",
                reply_markup=get_play_again_keyboard()
            )
            await state.clear()
            await state.set_state(None)
        else:
            # --- Изменено: Сразу отправляем следующий вопрос --- H
            # Убрали отправку "Готов к следующему?" и кнопки "Дальше"
            # Не сбрасываем состояние здесь, send_question сам установит GameState.in_game
            await send_question(chat_id, bot, state)
            # ----------------------------------------------------


# Обработчик для "Начать" / "Сыграть еще"
async def start_game_handler_local(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Начинает новую игру при нажатии кнопки 'Начать' или 'Сыграть еще'."""
    await callback.answer() # Отвечаем на колбэк
    if callback.message:
        # Пытаемся убрать клавиатуру из предыдущего сообщения (Начать или Сыграть еще)
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except TelegramBadRequest as e:
            print(f"Error editing message reply markup: {e}")

    # Перемешиваем типы моторов для нового раунда
    shuffled_engines = random.sample(ENGINE_TYPES, len(ENGINE_TYPES))

    # Сохраняем список вопросов и начальный счет в состояние
    await state.update_data(questions=shuffled_engines, score=0, question_index=0)

    # Отправляем первый вопрос
    if callback.message:
        await send_question(callback.message.chat.id, bot, state)

# Регистрируем локальный обработчик для callback_data="start_game"
callback_router.callback_query.register(start_game_handler_local, F.data == "start_game")

# Обработчик кнопки "Завершить"
@callback_router.callback_query(F.data == "quit_game")
async def quit_game_callback_handler(callback: CallbackQuery, state: FSMContext):
    """Завершает игру и очищает состояние."""
    await callback.answer()
    if callback.message:
        # Используем parse_mode=HTML для жирного шрифта
        await callback.message.edit_text("Спасибо за игру! 👋\nНадеюсь, тебе понравилось. До скорого!", parse_mode=ParseMode.HTML)
    await state.clear() 