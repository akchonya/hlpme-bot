import requests  # noqa

from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

register_router = Router()


@register_router.message(F.connected_website)
async def register_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    empty = "користувач ще не надав цю інформацію"
    request = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "full_name": empty,
        "email": empty,
        "phone_number": empty,
    }

    response = requests.post(
        "https://hlp-me-back.onrender.com/tg/register", json=request
    )
    status = int(response.status_code)

    print(status)

    if status == 400:
        await message.answer(
            "❕ ви вже були авторизовані!\nможете дозаповнити інформацію за допомогою /fill_data",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    print(response.json())

    await message.answer(
        "✅ дякую, ви успішно авторизувалися!\nможете дозаповнити інформацію за допомогою /fill_data",
        reply_markup=ReplyKeyboardRemove(),
    )
