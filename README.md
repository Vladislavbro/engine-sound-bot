# Угадай мотор по звуку - Телеграм бот

[![Бот в Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg?style=flat-square&logo=telegram)](https://t.me/engine_game_bot)

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

## ✨ Возможности

*   🎮 **Интерактивная игра:** Угадывай тип мотора по его звуку.
*   🔊 **Реальные звуки:** Используются качественные аудиозаписи.
*   🏆 **Подсчет очков:** Соревнуйся сам с собой или друзьями.
*   🖼️ **Персонализированные результаты:** Получи уникальную картинку с твоим результатом в конце игры.
*   📊 **Статистика игр:** Бот сохраняет старты и результаты игр в локальную базу данных SQLite (`stats.db`).
*   🔒 **Админ-панель (для владельца):** Команда `/stats` позволяет владельцу бота (чей Telegram ID указан в `.env`) просматривать статистику игр за разные периоды (сегодня, вчера, 7 дней, всё время).

## 🛠️ Технологии

*   **Язык:** Python
*   **Библиотека для Telegram Bot API:** [aiogram](https://github.com/aiogram/aiogram)
*   **Управление состояниями:** aiogram FSM (MemoryStorage)
*   **Конфигурация:** python-dotenv
*   **База данных:** SQLite (для хранения стартов и результатов игр)

---

## 🚀 Запуск

### 1. Локальный запуск (для разработки и тестирования)

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Vladislavbro/engine-sound-bot
    cd engine-sound-bot
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
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
    *   Добавьте в него строку с вашим токеном:
        ```env
        BOT_TOKEN=ВАШ_API_ТОКЕН_ЗДЕСЬ
        ```
    *   **(Опционально, для админ-функций)** Чтобы иметь доступ к команде `/stats`, добавьте ваш Telegram ID:
        ```env
        ADMIN_ID=ВАШ_ТЕЛЕГРАМ_ID
        ```
        *(Узнать свой ID можно, например, у бота [`@userinfobot`](https://t.me/userinfobot))*.

6.  **Скачайте медиафайлы:**
    *   Папку `media` (с подпапками `images` и `sounds`) **необходимо** скачать отдельно.
    *   **Скачайте архив** с Google Диска по [этой ссылке](https://drive.google.com/drive/folders/14VvhiuacMtXAzdNUyU3miyVc3bVPayEG?usp=sharing).
    *   **Распакуйте архив** и поместите папку `media` в корень проекта (`engine-sound-bot/media`).
    *   Убедитесь, что структура папок и имена файлов внутри `media/` соответствуют путям в файле `data.py`.

7.  **База данных:**
    *   При первом запуске бота (`python bot.py`) автоматически будет создан файл `stats.db` в корневой директории. Этот файл содержит статистику игр и добавлен в `.gitignore`.

8.  **Запустите бота:**
    ```bash
    python bot.py
    ```

9.  Найдите вашего бота в Telegram и начните с ним диалог.

### 2. Развертывание на сервере (Linux, Ubuntu/Debian)

Этот раздел описывает базовый способ развертывания бота на сервере с использованием `systemd` для управления процессом.

**Предварительные требования:**

*   Сервер под управлением Linux (например, Ubuntu 20.04/22.04 LTS).
*   Установленный Python 3, `pip` и `venv`:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y
    ```
*   Доступ к серверу по SSH.
*   Установленный `git`:
    ```bash
    sudo apt install git -y
    ```

**Шаги развертывания:**

1.  **Подключитесь к серверу по SSH.**

2.  **Клонируйте репозиторий:**
    *   Перейдите в директорию, где будет жить ваш бот (например, `/home/your_user/` или `/opt/`).
    *   Клонируйте репозиторий:
        ```bash
        git clone https://github.com/Vladislavbro/engine-sound-bot
        cd engine-sound-bot # Перейдите в папку проекта
        ```

3.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Создайте файл `.env`:**
    *   Создайте файл `.env` в корне проекта:
        ```bash
        nano .env
        ```
    *   Вставьте токен вашего бота и, опционально, ID администратора:
        ```env
        BOT_TOKEN=ВАШ_API_ТОКЕН_ЗДЕСЬ
        ADMIN_ID=ВАШ_ТЕЛЕГРАМ_ID # Опционально
        ```
    *   Сохраните файл (Ctrl+X, затем Y, затем Enter).

6.  **Загрузите медиафайлы:**
    *   Папку `media` **необходимо** скачать и загрузить отдельно.
    *   **Скачайте архив** с Google Диска по [этой ссылке](https://drive.google.com/drive/folders/14VvhiuacMtXAzdNUyU3miyVc3bVPayEG?usp=sharing).
    *   **Распакуйте архив** на своем локальном компьютере.
    *   **Загрузите** распакованную папку `media` на сервер в корневую директорию проекта (`/путь/к/engine-sound-bot/`) с помощью `scp` (команду выполнять на локальной машине):
        ```bash
        scp -r /путь/к/локальной/папке/media your_user@ВАШ_IP_СЕРВЕРА:/путь/к/engine-sound-bot/
        ```
        *(Замените `/путь/к/локальной/папке/media`, `your_user`, `ВАШ_IP_СЕРВЕРА` и `/путь/к/engine-sound-bot/` на ваши реальные значения).* 

7.  **Проверьте запуск бота вручную (опционально, но рекомендуется):**
    *   Убедитесь, что виртуальное окружение активно (`(venv)`).
    *   Запустите: `python bot.py`.
    *   Проверьте работу бота в Telegram, затем остановите (Ctrl+C).

8.  **Создайте сервис `systemd`:**
    *   Это позволит боту автоматически запускаться и перезапускаться.
    *   Создайте файл юнита:
        ```bash
        sudo nano /etc/systemd/system/engine-sound-bot.service
        ```
    *   Вставьте следующее содержимое, **внимательно заменив** `/путь/к/engine-sound-bot` на ваш реальный путь к проекту и `your_user` на имя пользователя, от которого будет работать бот:
        ```ini
        [Unit]
        Description=Engine Sound Telegram Bot
        After=network.target

        [Service]
        # Укажите пользователя и группу, если бот не должен работать от root
        User=your_user 
        Group=your_user 
        # Рабочая директория, где лежит bot.py
        WorkingDirectory=/путь/к/engine-sound-bot 
        # Полный путь к Python в venv и к bot.py
        ExecStart=/путь/к/engine-sound-bot/venv/bin/python bot.py 
        Restart=always
        RestartSec=10

        [Install]
        WantedBy=multi-user.target
        ```
    *   Сохраните файл (Ctrl+X, затем Y, затем Enter).

9.  **Настройте и запустите сервис:**
    *   Перезагрузите конфигурацию `systemd`:
        ```bash
        sudo systemctl daemon-reload
        ```
    *   Включите автозапуск сервиса при старте системы:
        ```bash
        sudo systemctl enable engine-sound-bot.service
        ```
    *   Запустите сервис:
        ```bash
        sudo systemctl start engine-sound-bot.service
        ```
    *   Проверьте статус сервиса:
        ```bash
        sudo systemctl status engine-sound-bot.service
        ```
        *(Должно быть `active (running)`. Нажмите `q` для выхода)*.

10. **Просмотр логов (при необходимости):**
    *   Для отслеживания работы или поиска ошибок:
        ```bash
        sudo journalctl -u engine-sound-bot.service -f
        ```
        *(Ключ `-f` для режима реального времени, Ctrl+C для выхода)*.

### 3. Обновление бота на сервере

1.  Подключитесь к серверу по SSH.
2.  Перейдите в директорию проекта:
    ```bash
    cd /путь/к/engine-sound-bot
    ```
3.  Получите последние изменения из Git:
    ```bash
    git pull origin main # Или ваша основная ветка
    ```
4.  Активируйте виртуальное окружение:
    ```bash
    source venv/bin/activate
    ```
5.  **(Важно!)** Обновите зависимости, если `requirements.txt` изменился:
    ```bash
    pip install -r requirements.txt
    ```
6.  Перезапустите сервис, чтобы применить изменения:
    ```bash
    sudo systemctl restart engine-sound-bot.service
    ```
7.  Проверьте статус и логи:
    ```bash
    sudo systemctl status engine-sound-bot.service
    sudo journalctl -u engine-sound-bot.service -n 50 # Последние 50 строк
    ```

Поздравляем! Ваш бот развернут и работает.