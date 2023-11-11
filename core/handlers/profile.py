from aiogram import Router, html, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

from ..db.base import collection


profile_router = Router()


@profile_router.message(Command("profile"))
async def profile_handler(message: types.Message):
    user = message.from_user
    user_db = await collection.find_one({"user_id": user.id})
    await message.answer(
        f"ваш профіль: \n" f"username: {user_db['username']}",
        reply_markup=ReplyKeyboardRemove(),
    )
