from aiogram.fsm.state import StatesGroup, State


class StatesLocation(StatesGroup):
    GET_LOCATION = State()
    CONFIRM_LOCATION = State()


class StatesNeedHelp(StatesGroup):
    GET_CAPTION = State()
    GET_DESCRIPTION = State()
    GET_LOCATION = State()
    GET_DATE = State()
    CHECK = State()
