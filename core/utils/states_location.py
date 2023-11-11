from aiogram.fsm.state import StatesGroup, State


class StatesLocation(StatesGroup):
    GET_LOCATION = State()
    CONFIRM_LOCATION = State()
