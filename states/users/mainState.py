from aiogram.dispatcher.filters.state import StatesGroup, State


class MainState(StatesGroup):
    Answer = State()