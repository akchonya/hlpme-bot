"""
/start greets a user and registers it in db
"""


from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove
from aiogram import html

from ..db.base import collection
from ..db.register import create_user, update_user

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: types.Message):
    user = message.from_user
    await update_user(user_id=user.id, username=user.username, collection=collection)
    await message.answer(
        f"добрий день! це ботік від команди {html.bold('💅🏻slay devs💅🏻')}",
        reply_markup=ReplyKeyboardRemove(),
    )
