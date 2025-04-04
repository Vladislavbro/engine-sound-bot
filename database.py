# -*- coding: utf-8 -*-
import sqlite3
import logging
from datetime import datetime

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

# Пример функции для получения статистики (можно добавить позже)
# def get_user_stats(user_id: int):
#     # ... (код для запроса статистики из БД) ...
#     pass 