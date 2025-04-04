# Инструкция по развертыванию бота на сервере

Это руководство описывает базовый способ развертывания телеграм-бота "Угадай мотор по звуку" на Linux-сервере (например, Ubuntu/Debian) с использованием `systemd` для управления процессом бота.

## Предварительные требования

*   Сервер под управлением Linux (например, Ubuntu 20.04/22.04 LTS).
*   Установленный Python 3 (обычно предустановлен) и `pip`.
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y
    ```
*   Доступ к серверу по SSH.
*   Установленный `git`.
    ```bash
    sudo apt install git -y
    ```

## Шаги развертывания

1.  **Подключитесь к серверу по SSH.**

2.  **Клонируйте репозиторий:**
    *   Перейдите в директорию, где будет жить ваш бот (например, `/home/your_user/bots`).
    *   Клонируйте репозиторий:
        ```bash
        git clone https://github.com/Vladislavbro/engine-sound-bot 
        cd engine-sound-bot
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
    *   Создайте файл `.env` в корне проекта (`engine-sound-bot/`):
        ```bash
        nano .env
        ```
    *   Вставьте ваш токен бота:
        ```env
        BOT_TOKEN=ВАШ_API_ТОКЕН_ЗДЕСЬ
        ```
    *   Сохраните файл (Ctrl+X, затем Y, затем Enter в `nano`).

6.  **Настройка systemd:**
    *   Скопируйте файл `engine-sound-bot.service` в `/etc/systemd/system/`.
    *   Перезагрузите конфигурацию systemd: `systemctl daemon-reload`
    *   Включите автозапуск сервиса: `systemctl enable engine-sound-bot`

7.  **Убедитесь, что медиафайлы на месте:**
    *   Папку `media` (с подпапками `images` и `sounds`) **необходимо** скачать отдельно, так как она не хранится в Git.
    *   **Скачайте архив** с папкой `media` с Google Диска по [этой ссылке](https://drive.google.com/drive/folders/14VvhiuacMtXAzdNUyU3miyVc3bVPayEG?usp=sharing).
    *   **Распакуйте архив** на своем локальном компьютере.
    *   **Загрузите** распакованную папку `media` на сервер в корневую директорию проекта (`/root/engine-sound-bot/`) с помощью `scp`. Выполните следующую команду **на своем локальном компьютере** (не на сервере), заменив `/путь/к/вашей/папке/media` на реальный путь, куда вы распаковали архив, а `ВАШ_IP_АДРЕС_СЕРВЕРА` на IP вашего сервера:
      ```bash
      scp -r /путь/к/вашей/папке/media root@ВАШ_IP_АДРЕС_СЕРВЕРА:/root/engine-sound-bot/
      ```
      *(Пример для сервера 176.113.83.24 и папки в Загрузках: `scp -r ~/Downloads/media root@176.113.83.24:/root/engine-sound-bot/`)*

8.  **Проверьте запуск бота вручную:**
    *   Убедитесь, что виртуальное окружение активировано (`(venv)` должно быть в начале строки терминала).
    *   Запустите бота:
        ```bash
        python bot.py
        ```
    *   Проверьте работу бота в Telegram. Остановите его (Ctrl+C).

9.  **Создайте сервис `systemd`:**
    *   `systemd` позволит боту автоматически запускаться при старте сервера и перезапускаться в случае сбоев.
    *   Создайте файл юнита для сервиса:
        ```bash
        sudo nano /etc/systemd/system/engine-sound-bot.service
        ```
    *   Вставьте следующее содержимое, **заменив `/home/your_user/bots/engine-sound-bot` на ваш реальный путь** к проекту и `your_user` на вашего пользователя:

        ```ini
        [Unit]
        Description=Engine Sound Telegram Bot
        After=network.target

        [Service]
        User=your_user
        Group=your_user
        WorkingDirectory=/home/your_user/bots/engine-sound-bot
        ExecStart=/home/your_user/bots/engine-sound-bot/venv/bin/python bot.py
        Restart=always
        RestartSec=10

        [Install]
        WantedBy=multi-user.target
        ```

    *   **Объяснение полей:**
        *   `Description`: Описание сервиса.
        *   `After=network.target`: Запускать после того, как сеть станет доступна.
        *   `User`, `Group`: Пользователь и группа, от имени которых будет запускаться бот.
        *   `WorkingDirectory`: Рабочая директория проекта (где лежит `bot.py`).
        *   `ExecStart`: Полный путь к интерпретатору Python **внутри виртуального окружения** и путь к главному файлу бота.
        *   `Restart=always`: Всегда перезапускать сервис, если он упал.
        *   `RestartSec=10`: Пауза в 10 секунд перед перезапуском.
        *   `WantedBy=multi-user.target`: Включить сервис для многопользовательского режима.

    *   Сохраните файл (Ctrl+X, затем Y, затем Enter).

10. **Просмотр логов (при необходимости):**
    *   Если бот не работает или есть ошибки, можно посмотреть логи сервиса:
        ```bash
        sudo journalctl -u engine-sound-bot.service -f
        ```
        Ключ `-f` позволяет следить за логами в реальном времени (Ctrl+C для выхода).

## Обновление бота

1.  Подключитесь к серверу.
2.  Перейдите в директорию проекта:
    ```bash
    cd /home/your_user/bots/engine-sound-bot
    ```
3.  Остановите сервис:
    ```bash
    sudo systemctl stop engine-sound-bot.service
    ```
4.  Получите последние изменения из Git:
    ```bash
    git pull origin main # Или ваша основная ветка
    ```
5.  Активируйте виртуальное окружение:
    ```bash
    source venv/bin/activate
    ```
6.  Обновите зависимости, если `requirements.txt` изменился:
    ```bash
    pip install -r requirements.txt
    ```
7.  Деактивируйте окружение (не обязательно, но для чистоты):
    ```bash
    deactivate
    ```
8.  Запустите сервис снова:
    ```bash
    sudo systemctl start engine-sound-bot.service
    ```
9.  Проверьте статус:
    ```bash
    sudo systemctl status engine-sound-bot.service
    ```

Поздравляем! Ваш бот развернут и работает на сервере. 