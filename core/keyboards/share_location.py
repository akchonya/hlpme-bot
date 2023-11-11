from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


share_location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="поділитися локацією", request_location=True),
        ]
    ],
    resize_keyboard=True,
)
