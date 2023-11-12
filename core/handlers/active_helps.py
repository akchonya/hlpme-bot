import requests
from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message
from geopy.geocoders import Nominatim

active_helps_router = Router()


@active_helps_router.message(Command("active_helps"))
async def active_helps_handler(message: Message):
    response = requests.get("https://hlp-me-back.onrender.com/local/dangers")
    response_status = int(response.status_code)
    print(response_status)

    if response_status == 500:
        await message.answer(
            "наразі сервіс недоступний, перепрошуємо за незручності 😩\nспробуйте пізніше"
        )
        return

    response = response.json()
    print(response)
    msg = ""
    for i in range(len(response)):
        help = response[i]
        latitude = help["coordinates"]["latitude"]
        longitude = help["coordinates"]["longitude"]

        geolocator = Nominatim(user_agent="test_tg_bot")
        location = geolocator.reverse(f"{latitude},{longitude}")
        address = location.raw["address"]
        city = address.get("city", "")

        print(help)
        msg += f"{i+1}. {html.bold(help['name'])}\n"
        msg += f"{help['description']}\n"
        msg += f'🗺 місто:  <a href="https://www.google.com/maps?q={latitude},{longitude}">{city}</a>\n'
        msg += f"📅 на коли: {str(help['date_time'])[:10]}\n"
        msg += (
            f"📲 <a href=\"tg://user?id={help['user']['user_id']}\">зв'язатися</a>\n\n"
        )

    await message.answer(msg, disable_web_page_preview=True)
