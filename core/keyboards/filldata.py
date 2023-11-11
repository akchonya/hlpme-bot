from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


share_phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="поділитися номером тф", request_contact=True),
        ]
    ],
    resize_keyboard=True,
)


confirm_fill_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="confirm"),
            InlineKeyboardButton(text="❌", callback_data="decline"),
        ]
    ]
)
