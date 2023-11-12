"""
/start greets a user
"""


from aiogram import Router, html, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        f"добрий день! це ботік від команди {html.bold('💅🏻slay devs💅🏻')}",
        reply_markup=ReplyKeyboardRemove(),
    )
