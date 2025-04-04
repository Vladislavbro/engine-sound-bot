# -*- coding: utf-8 -*-
import sqlite3
import logging
from datetime import datetime, timedelta

DATABASE_NAME = "stats.db"

def init_db():
    """Инициализирует базу данных и создает таблицы, если они не существуют."""
    conn = None # Инициализируем conn
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        # Включаем поддержку внешних ключей (важно для SQLite)
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Таблица для стартов игры
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_starts (
                start_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                start_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица для результатов завершенных игр
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL, 
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                finish_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (start_id) REFERENCES game_starts(start_id)
            )
        """)
        conn.commit()
        logging.info(f"Database {DATABASE_NAME} initialized successfully (game_starts, game_results tables)." )
    except sqlite3.Error as e:
        logging.error(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def log_game_start(user_id: int) -> int | None:
    """Логирует старт новой игры и возвращает ID старта."""
    conn = None
    start_id = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO game_starts (user_id, start_timestamp)
            VALUES (?, ?)
        """, (user_id, datetime.now()))
        conn.commit()
        start_id = cursor.lastrowid # Получаем ID только что вставленной записи
        logging.info(f"Game start logged for user {user_id}. start_id: {start_id}")
    except sqlite3.Error as e:
        logging.error(f"Error logging game start for user {user_id}: {e}")
    finally:
        if conn:
            conn.close()
    return start_id

def log_game_result(start_id: int, user_id: int, score: int, total_questions: int):
    """Логирует результат завершенной игры."""
    conn = None
    if start_id is None:
        logging.error(f"Cannot log game result for user {user_id} without a start_id.")
        return
        
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO game_results (start_id, user_id, score, total_questions, finish_timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (start_id, user_id, score, total_questions, datetime.now()))
        conn.commit()
        logging.info(f"Game result logged for start_id {start_id} (user {user_id}): {score}/{total_questions}")
    except sqlite3.Error as e:
        logging.error(f"Error logging game result for start_id {start_id} (user {user_id}): {e}")
    finally:
        if conn:
            conn.close()

# --- Добавлено: Функции для получения статистики ---

def _get_time_range(period: str) -> tuple[datetime | None, datetime | None]:
    """Возвращает начальную и конечную дату для заданного периода."""
    now = datetime.now()
    if period == "today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    elif period == "yesterday":
        end_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=1)
    elif period == "7days":
        end_date = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1) # Включая сегодня
        start_date = end_date - timedelta(days=7)
    elif period == "all":
        start_date = None
        end_date = None
    else:
        raise ValueError(f"Неизвестный период: {period}")
    return start_date, end_date

def get_stats(period: str = "all") -> dict:
    """
    Собирает статистику по играм за указанный период.

    Args:
        period (str): Период для сбора статистики ("today", "yesterday", "7days", "all").
                       По умолчанию "all".

    Returns:
        dict: Словарь со статистикой:
              {
                  'total_starts': int,
                  'unique_starters': int,
                  'total_finishes': int,
                  'unique_finishers': int,
                  'average_score': float | None
              }
    """
    conn = None
    try:
        start_dt, end_dt = _get_time_range(period)
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        stats = {
            "total_starts": 0,
            "unique_starters": 0,
            "total_finishes": 0,
            "unique_finishers": 0,
            "average_score": None
        }

        # --- Подсчет стартов ---
        query_starts = "SELECT COUNT(*), COUNT(DISTINCT user_id) FROM game_starts"
        params_starts = []
        if start_dt and end_dt:
            query_starts += " WHERE datetime(start_timestamp) >= datetime(?) AND datetime(start_timestamp) < datetime(?)"
            params_starts.extend([start_dt.isoformat(), end_dt.isoformat()])

        cursor.execute(query_starts, params_starts)
        result_starts = cursor.fetchone()
        if result_starts:
            stats["total_starts"] = result_starts[0]
            stats["unique_starters"] = result_starts[1]

        # --- Подсчет финишей и среднего балла ---
        query_results = "SELECT COUNT(*), COUNT(DISTINCT user_id), AVG(score) FROM game_results"
        params_results = []
        if start_dt and end_dt:
            query_results += " WHERE datetime(finish_timestamp) >= datetime(?) AND datetime(finish_timestamp) < datetime(?)"
            params_results.extend([start_dt.isoformat(), end_dt.isoformat()])

        cursor.execute(query_results, params_results)
        result_results = cursor.fetchone()
        if result_results:
            stats["total_finishes"] = result_results[0]
            stats["unique_finishers"] = result_results[1]
            # AVG вернет None, если нет строк, соответствующих WHERE
            stats["average_score"] = result_results[2] if result_results[2] is not None else 0

        logging.info(f"Статистика за период '{period}' ({start_dt} - {end_dt}): {stats}")
        return stats

    except sqlite3.Error as e:
        logging.error(f"Ошибка SQLite при получении статистики за период '{period}': {e}")
        # Возвращаем пустую статистику или пробрасываем исключение?
        # Пока вернем пустую
        return {
            "total_starts": 0,
            "unique_starters": 0,
            "total_finishes": 0,
            "unique_finishers": 0,
            "average_score": None
        }
    except ValueError as e:
        logging.error(f"Ошибка при расчете диапазона времени для статистики: {e}")
        # Возвращаем пустую статистику при неверном периоде
        return {
            "total_starts": 0,
            "unique_starters": 0,
            "total_finishes": 0,
            "unique_finishers": 0,
            "average_score": None
        }
    finally:
        if conn:
            conn.close()

