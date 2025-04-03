# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# TODO: Создать клавиатуру для старта игры
def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Начать", callback_data="start_game"))
    return builder.as_markup()

# TODO: Создать клавиатуру с вариантами ответов
def get_game_keyboard(options: list[str], correct_answer: str) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру с 4 вариантами ответа."""
    builder = InlineKeyboardBuilder()
    for option in options:
        # В callback_data можно передать и правильный ответ для проверки
        builder.add(InlineKeyboardButton(
            text=option,
            callback_data=f"answer:{option}:{correct_answer}" # Пример callback_data
        ))
    # Располагаем кнопки, например, по 2 в ряд
    builder.adjust(2)
    return builder.as_markup()

# TODO: Создать клавиатуру "Сыграть еще?"
def get_play_again_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Сыграть ещё", callback_data="start_game"),
        InlineKeyboardButton(text="Завершить", callback_data="quit_game")
    )
    return builder.as_markup() 