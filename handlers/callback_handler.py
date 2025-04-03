# -*- coding: utf-8 -*-
import random # Добавили импорт random
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

# TODO: Импортировать необходимые данные, клавиатуры, состояния
# from data import ENGINES_DATA
# from keyboards import get_next_keyboard
# from states import GameState

# Импортируем необходимые данные, клавиатуры, состояния
from data import ENGINES_DATA, ENGINE_TYPES # Добавили ENGINE_TYPES
from keyboards import get_next_keyboard, get_play_again_keyboard # Добавили get_play_again_keyboard
from states import GameState
# Импортируем функцию отправки вопроса для кнопки "Дальше"
from handlers.game_handler import send_question

callback_router = Router() # Создаем роутер для этого хэндлера

# Обработчик колбэков с ответами (срабатывает в состоянии in_game)
@callback_router.callback_query(F.data.startswith("answer:"), GameState.in_game)
async def process_answer_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Обрабатывает ответ пользователя."""
    await callback.answer() # Отвечаем на колбэк, чтобы убрать "часики"

    # Извлекаем данные из callback_data
    # Формат: "answer:выбранный_ответ:правильный_ответ"
    _, selected_option, correct_answer = callback.data.split(":")

    user_data = await state.get_data()
    current_score = user_data.get('score', 0)
    question_index = user_data.get('question_index', 0) # Получаем текущий индекс ВОПРОСА (он уже +1 от реального)
    question_list = user_data.get('questions', [])
    total_questions = len(question_list)

    engine_info = ENGINES_DATA[correct_answer]
    # Убрали sound, так как он больше не нужен здесь
    image = FSInputFile(engine_info["image_file"])
    result_message = ""

    if selected_option == correct_answer:
        result_message = f"✅ Правильно! Это {correct_answer} ({engine_info['car']})."
        current_score += 1
        # Обновляем счет СРАЗУ, чтобы он был правильным для финального сообщения
        await state.update_data(score=current_score)
    else:
        result_message = f"❌ Неправильно. Это был {correct_answer} ({engine_info['car']})."

    if callback.message:
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except TelegramBadRequest as e:
            print(f"Error editing message reply markup: {e}")

        # Отправляем результат и картинку
        await bot.send_message(callback.message.chat.id, result_message)
        await bot.send_photo(callback.message.chat.id, photo=image)

        # --- Добавлено: Проверка на последний вопрос --- H
        # question_index содержит номер СЛЕДУЮЩЕГО вопроса (т.к. мы делаем +1 в send_question)
        # Значит, если он равен total_questions, текущий ответ был на последний вопрос.
        if question_index >= total_questions:
            # Сразу показываем финальный результат
            await bot.send_message(
                callback.message.chat.id,
                f"\n\nИгра окончена! Твой результат: {current_score} из {total_questions} угаданных моторов.",
                reply_markup=get_play_again_keyboard()
            )
            await state.clear()
            await state.set_state(None)
        else:
            # Если это был НЕ последний вопрос, отправляем кнопку "Дальше"
            await bot.send_message(callback.message.chat.id, "\n\nГотов к следующему?", reply_markup=get_next_keyboard())
            await state.set_state(None) # Сбрасываем состояние для кнопки "Дальше"
        # --------------------------------------------------


# Обработчик кнопки "Дальше" (callback_data="next_question")
@callback_router.callback_query(F.data == "next_question")
async def next_question_callback_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Отправляет следующий вопрос при нажатии 'Дальше'."""
    await callback.answer()
    if callback.message:
        # Убираем кнопку "Дальше"
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except TelegramBadRequest as e:
            print(f"Error editing message reply markup: {e}")
        # Отправляем следующий вопрос
        await send_question(callback.message.chat.id, bot, state)


# Определяем обработчик для "Начать" / "Сыграть еще" прямо здесь
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
        await callback.message.edit_text("Спасибо за игру! До свидания!") # Редактируем сообщение
    await state.clear() 