from aiogram.fsm.state import State, StatesGroup


class StatesFill(StatesGroup):
    GET_FULLNAME = State()
    GET_EMAIL = State()
    GET_PHONE = State()
    CHECK = State()
