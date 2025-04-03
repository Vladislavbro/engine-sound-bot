# -*- coding: utf-8 -*-

# Словарь с данными о моторах, машинах, звуках и картинках
# Ключ - тип мотора, значение - словарь с деталями

ENGINES_DATA = {
    "Flat-6": {
        "car": "Porsche 911 GT3",
        "sound_file": "media/sounds/porsche_911_gt3.mp3",
        "image_file": "media/images/porsche_911_gt3.jpg"
    },
    "I6": {
        "car": "BMW M3 (E46)",
        "sound_file": "media/sounds/bmw_m3_e46.mp3",
        "image_file": "media/images/bmw_m3_e46.jpg"
    },
    "V6": {
        "car": "Nissan GT-R r35",
        "sound_file": "media/sounds/nissan_gtr_r35.mp3",
        "image_file": "media/images/nissan_gtr_r35.jpg"
    },
    "Турбо V8": {
        "car": "Maserati Quattroporte",
        "sound_file": "media/sounds/maserati_quattroporte.mp3",
        "image_file": "media/images/maserati_quattroporte.jpg"
    },
    "Атмо V8": {
        "car": "Ferrari 458",
        "sound_file": "media/sounds/ferrari_458.mp3",
        "image_file": "media/images/ferrari_458.jpg"
    },
    "V10": {
        "car": "Lexus LFA",
        "sound_file": "media/sounds/lexus_lfa.mp3",
        "image_file": "media/images/lexus_lfa.jpg"
    },
    "Атмо V12": {
        "car": "Ferrari F12 Berlinetta",
        "sound_file": "media/sounds/ferrari_f12.mp3",
        "image_file": "media/images/ferrari_f12.jpg"
    },
    "V16": {
        "car": "Bugatti Tourbillon",
        "sound_file": "media/sounds/bugatti_tourbillon.mp3",
        "image_file": "media/images/bugatti_tourbillon.jpg"
    }
}

# Получаем список всех 8 типов моторов
ENGINE_TYPES = list(ENGINES_DATA.keys())

# Убедитесь, что у вас есть папка 'media' с подпапками 'sounds' и 'images'
# и что файлы в них названы так, как указано выше. 