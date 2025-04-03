# -*- coding: utf-8 -*-
import random
from data import ENGINE_TYPES

def get_random_options(correct_answer: str, all_options: list[str], num_options: int = 4) -> list[str]:
    """Выбирает случайные варианты ответа, включая правильный."""
    options = [correct_answer]
    # Убираем правильный ответ из списка всех вариантов
    other_options = [opt for opt in all_options if opt != correct_answer]
    # Добавляем нужное количество неправильных ответов
    options.extend(random.sample(other_options, num_options - 1))
    # Перемешиваем итоговый список
    random.shuffle(options)
    return options

# Можно добавить сюда другие утилиты, например, для работы с FSM 