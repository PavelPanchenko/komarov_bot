from aiogram.dispatcher.filters.state import StatesGroup, State


class Appointments(StatesGroup):
    time = State()
    file = State()


class Support(StatesGroup):
    active = State()


class MessageAll(StatesGroup):
    message = State()
