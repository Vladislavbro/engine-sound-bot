# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
# Добавляем импорт основного словаря
from data import ENGINES_DATA

# TODO: Создать клавиатуру для старта игры
def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Начать", callback_data="start_game"))
    return builder.as_markup()

# TODO: Создать клавиатуру с вариантами ответов
def get_game_keyboard(options: list[str], correct_answer: str) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру с 4 вариантами ответа."""
    builder = InlineKeyboardBuilder()
    for option_key in options: # option_key теперь - это идентификатор, например "V8_Supercharged"
        # Получаем отображаемое имя из словаря данных
        display_name = ENGINES_DATA[option_key].get("display_name", option_key)
        builder.add(InlineKeyboardButton(
            text=display_name, # Используем display_name для текста
            callback_data=f"answer:{option_key}:{correct_answer}" # В callback используем простой ключ
        ))
    builder.adjust(2)
    return builder.as_markup()

# TODO: Создать клавиатуру "Сыграть еще?"
def get_play_again_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Сыграть ещё", callback_data="play_again")
    )
    return builder.as_markup()

# --- Добавлено: Клавиатура для выбора периода статистики ---
def stats_period_keyboard() -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру для выбора периода статистики."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Сегодня", callback_data="stats:today"),
        InlineKeyboardButton(text="📈 Вчера", callback_data="stats:yesterday")
    )
    builder.row(
        InlineKeyboardButton(text="🗓️ 7 дней", callback_data="stats:7days"),
        InlineKeyboardButton(text="🌍 Всё время", callback_data="stats:all")
    )
    return builder.as_markup() 