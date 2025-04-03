# -*- coding: utf-8 -*-

# Словарь с данными о моторах, машинах, звуках и картинках
# Ключ - тип мотора, значение - словарь с деталями

ENGINES_DATA = {
    "Flat-6": {
        "car": "Porsche 911 GT3",
        "sound_file": "sounds/flat_6.ogg",
        "image_file": "images/porsche_911_gt3.jpg"
    },
    "I6": {
        "car": "BMW M3 (E46)",
        "sound_file": "sounds/i6.ogg",
        "image_file": "images/bmw_m3_e46.jpg"
    },
    "V6": {
        "car": "Nissan GT-R",
        "sound_file": "sounds/v6.ogg",
        "image_file": "images/nissan_gtr.jpg"
    },
    "Турбо V8": {
        "car": "Porsche 911 Turbo",
        "sound_file": "sounds/turbo_v8.ogg",
        "image_file": "images/porsche_911_turbo.jpg"
    },
    "Атмо V8": {
        "car": "Ferrari 458",
        "sound_file": "sounds/atmo_v8.ogg",
        "image_file": "images/ferrari_458.jpg"
    },
    "V10": {
        "car": "Lamborghini Huracan Performante",
        "sound_file": "sounds/v10.ogg",
        "image_file": "images/lambo_huracan.jpg"
    },
    "Турбо V12": {
        "car": "Mercedes-AMG S65",
        "sound_file": "sounds/turbo_v12.ogg",
        "image_file": "images/merc_s65.jpg"
    },
    "Атмо V12": {
        "car": "Ferrari 812 Superfast",
        "sound_file": "sounds/atmo_v12.ogg",
        "image_file": "images/ferrari_812.jpg"
    },
    "W12": {
        "car": "Bentley Continental GT",
        "sound_file": "sounds/w12.ogg",
        "image_file": "images/bentley_gt.jpg"
    },
    "W16": {
        "car": "Bugatti Chiron",
        "sound_file": "sounds/w16.ogg",
        "image_file": "images/bugatti_chiron.jpg"
    }
}

# Получаем список всех типов моторов
ENGINE_TYPES = list(ENGINES_DATA.keys())

# TODO: Убедитесь, что пути к файлам звуков и картинок верны
# и что эти файлы существуют в соответствующих директориях. 