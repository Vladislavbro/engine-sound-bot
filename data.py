# -*- coding: utf-8 -*-

# Словарь с данными о моторах, машинах, звуках и картинках
# Ключ - простой идентификатор, значение - словарь с деталями

ENGINES_DATA = {
    "Flat-6": {
        "display_name": "Flat-6", # Отображаемое имя
        "car": "Porsche 911 GT3",
        "sound_file": "media/sounds/porsche_911_gt3.mp3",
        "image_file": "media/images/porsche_911_gt3.jpg" # Оставляем jpg
    },
    "I6": {
        "display_name": "I6",
        "car": "BMW M3 (E46)",
        "sound_file": "media/sounds/bmw_m3_e46.mp3",
        "image_file": "media/images/bmw_m3_e46.jpg" # Оставляем jpg
    },
    "V6": {
        "display_name": "V6",
        "car": "Nissan GT-R r35",
        "sound_file": "media/sounds/nissan_gtr_r35.mp3",
        "image_file": "media/images/nissan_gtr_r35.jpg" # Оставляем jpg
    },
    "V8_Supercharged": { # Простой ключ (идентификатор)
        "display_name": "V8 с нагнетателем", # Отображаемое имя
        "car": "Ford Mustang Shelby GT500",
        "sound_file": "media/sounds/Ford Mustang Shelby GT500.mp3",
        "image_file": "media/images/Ford Mustang Shelby GT500.webp" # Оставляем webp
    },
    "Atmo_V8": { # Простой ключ
        "display_name": "Атмо V8",
        "car": "Ferrari 458",
        "sound_file": "media/sounds/ferrari_458.mp3",
        "image_file": "media/images/ferrari_458.jpg" # Оставляем jpg
    },
    "V10": {
        "display_name": "V10",
        "car": "Lexus LFA",
        "sound_file": "media/sounds/lexus_lfa.mp3",
        "image_file": "media/images/lexus_lfa.jpeg" # Оставляем jpeg
    },
    "Atmo_V12": { # Простой ключ
        "display_name": "Атмо V12",
        "car": "Ferrari F12 Berlinetta",
        "sound_file": "media/sounds/ferrari_f12.mp3",
        "image_file": "media/images/ferrari_f12.jpeg" # Оставляем jpeg
    },
    "V16": {
        "display_name": "V16",
        "car": "Bugatti Tourbillon",
        "sound_file": "media/sounds/bugatti_tourbillon.mp3",
        "image_file": "media/images/bugatti_tourbillon.jpg" # Оставляем jpg
    }
}

# Получаем список идентификаторов моторов
ENGINE_TYPES = list(ENGINES_DATA.keys())

# Убедитесь, что у вас есть папка 'media' с подпапками 'sounds' и 'images'
# и что файлы в них названы так, как указано выше. 