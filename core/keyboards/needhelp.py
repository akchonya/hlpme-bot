from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


share_location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="поділитися локацією", request_location=True),
        ]
    ],
    resize_keyboard=True,
)


confirm_help_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="help_confirm"),
            InlineKeyboardButton(text="❌", callback_data="help_decline"),
        ]
    ]
)
