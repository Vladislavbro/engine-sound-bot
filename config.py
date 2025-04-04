import os
from dotenv import load_dotenv

load_dotenv() # Загружаем переменные окружения из .env файла

# --- Считываем токены ---
# Переименуем основной токен, чтобы не было конфликта
MAIN_BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN_DEBUG = os.getenv("BOT_TOKEN_DEBUG")
print(f"[DEBUG] Loaded MAIN_BOT_TOKEN: {'Set' if MAIN_BOT_TOKEN else 'Not set'}")
print(f"[DEBUG] Loaded BOT_TOKEN_DEBUG: {'Set' if BOT_TOKEN_DEBUG else 'Not set'}")

# --- ID администратора ---
ADMIN_ID = os.getenv("ADMIN_ID")

# --- Выбираем токен для использования ---
USE_DEBUG_TOKEN = True # Поставь False перед деплоем на сервер

# Теперь BOT_TOKEN будет содержать актуальный токен
if USE_DEBUG_TOKEN:
    BOT_TOKEN = BOT_TOKEN_DEBUG
    print("[INFO] Using DEBUG token.")
else:
    BOT_TOKEN = MAIN_BOT_TOKEN
    print("[INFO] Using MAIN token.")

# --- Проверки ---
# Проверка наличия используемого токена (теперь проверяем BOT_TOKEN)
if not BOT_TOKEN:
    if USE_DEBUG_TOKEN:
        raise ValueError("Не задан BOT_TOKEN_DEBUG в .env и USE_DEBUG_TOKEN=True!")
    else:
        raise ValueError("Не задан BOT_TOKEN в .env и USE_DEBUG_TOKEN=False!")

# Проверка наличия ADMIN_ID
if not ADMIN_ID:
    print("[WARN] ADMIN_ID не задан в .env! Функции администратора не будут работать.")
    ADMIN_ID = None # Явно устанавливаем None, если ID не задан
else:
    try:
        ADMIN_ID = int(ADMIN_ID) # Преобразуем ID в число
    except ValueError:
        ADMIN_ID = None # Считаем невалидный ID как отсутствующий
        print("[WARN] ADMIN_ID в .env не является числом! Функции администратора не будут работать.")
        # raise ValueError("ADMIN_ID в .env должен быть числом!") # Или можно бросать ошибку

print(f"Загружен конфиг. Admin ID: {ADMIN_ID if ADMIN_ID else 'Не задан'}")