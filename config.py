import os
from dotenv import load_dotenv

load_dotenv()

# --- Отладка: Печатаем значение, полученное из окружения --- H
# Читаем дебажный токен
loaded_token = os.getenv("BOT_TOKEN_DEBUG") 
print(f"[DEBUG] Token loaded from environment (DEBUG): {loaded_token}")
# ----------------------------------------------------------

# Если дебажный токен не найден, пробуем основной (на всякий случай)
if not loaded_token:
    print("[WARN] BOT_TOKEN_DEBUG not found in .env, trying BOT_TOKEN...")
    loaded_token = os.getenv("BOT_TOKEN")
    print(f"[DEBUG] Token loaded from environment (MAIN): {loaded_token}")

BOT_TOKEN = loaded_token # Используем загруженное значение

# Добавьте сюда другие конфигурационные переменные, если понадобятся