from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


async def delete_help(names: list):
    kb = []
    for name in names:
        kb.append([KeyboardButton(text=name)])
    delete_help_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return delete_help_kb


confirm_delete_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="delete_confirm"),
            InlineKeyboardButton(text="❌", callback_data="delete_decline"),
        ]
    ]
)
