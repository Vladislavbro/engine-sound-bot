# Угадай мотор по звуку - Телеграм бот

[![Бот в Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg?style=flat-square&logo=telegram)](https://t.me/YourBotUsername) <!-- Замените YourBotUsername на имя вашего бота -->

Телеграм-бот, предлагающий увлекательную игру: угадать тип автомобильного мотора по его характерному звуку.

## 🎮 Об игре

*   **Цель:** Прослушать звук мотора и выбрать правильный тип из 4 предложенных вариантов.
*   **Вопросы:** Всего 8 вопросов, по одному на каждый уникальный тип мотора.
*   **Варианты моторов:** Flat-6, I6, V6, V8 с нагнетателем, Атмо V8, V10, Атмо V12, V16.
*   **Игровой процесс:**
    1.  Бот присылает картинку-заглушку и звук мотора.
    2.  Вы выбираете один из 4 вариантов ответа.
    3.  Бот сообщает, правильный ли ответ, показывает картинку соответствующей машины и дает послушать звук еще раз.
    4.  После 8 вопросов игра завершается, и бот показывает ваш результат с забавным сообщением и картинкой в зависимости от количества правильных ответов.
*   **Повторная игра:** Для начала новой игры необходимо очистить историю чата с ботом и снова отправить команду `/start`.

## 🛠️ Технологии

*   **Язык:** Python
*   **Библиотека для Telegram Bot API:** [aiogram](https://github.com/aiogram/aiogram)
*   **Управление состояниями:** aiogram FSM (MemoryStorage)
*   **Конфигурация:** python-dotenv

## ⚙️ Локальный запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/your_username/engine-sound-bot.git # Замените на ваш URL
    cd engine-sound-bot
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    # venv\Scripts\activate  # Для Windows
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Получите токен бота:**
    *   Создайте нового бота или используйте существующего через [@BotFather](https://t.me/BotFather) в Telegram.
    *   Скопируйте полученный API токен.

5.  **Создайте файл `.env`:**
    *   В корне проекта создайте файл с именем `.env`.
    *   Добавьте в него строку, заменив `ВАШ_API_ТОКЕН_ЗДЕСЬ` на ваш реальный токен:
        ```env
        BOT_TOKEN=ВАШ_API_ТОКЕН_ЗДЕСЬ
        ```

6.  **Подготовьте медиафайлы:**
    *   Убедитесь, что в директории `media/images/` находятся все необходимые изображения (машины, обложка `cover.png`, заглушка `unknown_engine.png`, финальные `lada.jpeg`, `miata.jpeg`, `daytona.jpeg`).
    *   Убедитесь, что в директории `media/sounds/` находятся все звуковые файлы моторов (`.mp3`).
    *   Имена файлов должны точно совпадать с путями, указанными в файле `data.py`.

7.  **Запустите бота:**
    ```bash
    python bot.py
    ```

8.  **Найдите бота в Telegram** по его имени пользователя и отправьте команду `/start`.

## 🤝 Участие

Предложения и пул-реквесты приветствуются! Если вы нашли ошибку или хотите предложить улучшение, пожалуйста, создайте Issue.

## Лицензия

[MIT](./LICENSE) <!-- Если у вас есть файл LICENSE, иначе можно убрать --> 