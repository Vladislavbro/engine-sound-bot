import logging
from aiogram import Router, F, types
from aiogram.filters import Command

from config import ADMIN_ID # Импортируем ID админа
from database import get_stats # Импортируем функцию получения статистики
from keyboards import stats_period_keyboard # Импортируем клавиатуру

admin_router = Router()

# Фильтр для проверки, является ли пользователь админом
# Важно: сравниваем с int(ADMIN_ID), т.к. из config он может прийти как строка
# Хотя мы в config.py уже преобразовали, лучше перестраховаться
# Обновление: В config.py уже преобразуется в int, можно просто ADMIN_ID
class AdminFilter:
    def __call__(self, message: types.Message | types.CallbackQuery) -> bool:
        # Проверяем, что ADMIN_ID вообще задан
        if not ADMIN_ID:
            logging.warning("Попытка использовать админ-команду, но ADMIN_ID не задан в конфиге.")
            return False
        # Проверяем ID пользователя
        is_admin = message.from_user.id == ADMIN_ID
        if not is_admin:
            logging.warning(f"Пользователь {message.from_user.id} попытался использовать админ-команду.")
        return is_admin

# Обработчик команды /stats
@admin_router.message(Command("stats"), AdminFilter())
async def cmd_stats(message: types.Message):
    """Отправляет сообщение с кнопками для выбора периода статистики."""
    logging.info(f"Администратор {message.from_user.id} запросил статистику.")
    await message.answer(
        "Выберите период для просмотра статистики:",
        reply_markup=stats_period_keyboard()
    )

# Обработчик колбэков для кнопок статистики (префикс "stats:")
@admin_router.callback_query(F.data.startswith("stats:"), AdminFilter())
async def process_stats_period(callback: types.CallbackQuery):
    """Обрабатывает выбор периода и отправляет статистику."""
    period = callback.data.split(":")[1]
    user_id = callback.from_user.id
    logging.info(f"Администратор {user_id} запросил статистику за период '{period}'.")

    # Получаем статистику из БД
    stats_data = get_stats(period)

    # Формируем сообщение
    period_text = {
        "today": "Сегодня",
        "yesterday": "Вчера",
        "7days": "Последние 7 дней",
        "all": "Всё время"
    }.get(period, "Неизвестный период")

    avg_score = stats_data["average_score"]
    # Исправляем форматирование: показываем 0.0, если средний балл равен 0
    avg_score_text = f"{avg_score:.1f}" if avg_score is not None else "-"

    response_text = (
        f"📊 **Статистика за период: {period_text}**\n\n"
        f"▶️ **Старты игры:**\n"
        f"  - Всего: {stats_data['total_starts']}\n"
        f"  - Уникальных игроков: {stats_data['unique_starters']}\n\n"
        f"🏁 **Завершения игры:**\n"
        f"  - Всего: {stats_data['total_finishes']}\n"
        f"  - Уникальных игроков: {stats_data['unique_finishers']}\n\n"
        f"🏆 **Средний балл:** {avg_score_text}"
    )

    try:
        # Отвечаем на колбэк, чтобы убрать часики у кнопки
        await callback.answer()
        # Отправляем сообщение со статистикой
        # Используем edit_text для замены сообщения с кнопками
        await callback.message.edit_text(response_text, parse_mode="Markdown")
        # Если хочешь отправлять новым сообщением, используй:
        # await callback.message.answer(response_text, parse_mode="Markdown")
        # await callback.message.delete() # Удалить старое с кнопками
    except Exception as e:
        logging.error(f"Ошибка при отправке статистики администратору {user_id}: {e}")
        await callback.answer("Произошла ошибка при получении статистики.", show_alert=True) 