from aiogram.fsm.state import StatesGroup, State


class StatesDelete(StatesGroup):
    GET_HELP = State()
    CONFIRM = State()
