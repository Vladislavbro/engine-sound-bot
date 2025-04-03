# -*- coding: utf-8 -*-
from aiogram.fsm.state import State, StatesGroup

class GameState(StatesGroup):
    in_game = State()       # Состояние, когда пользователь находится в игре (ожидает ответа)
    # Можно добавить другие состояния при необходимости, например, ожидание нажатия "Дальше" 