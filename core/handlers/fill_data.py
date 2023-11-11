import requests

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove

from geopy.geocoders import Nominatim

from core.keyboards.share_location import share_location_kb
from core.utils.states_location import StatesLocation
from core.db.base import collection
from core.utils.config import ADMIN_ID
from core.db.register import update_user

fill_data = Router()


# Ask user for their location
@fill_data.message(Command("share_location"))
async def share_location_handler(message: Message, state: FSMContext):
    await message.answer(
        "поділіться вашою локацією, будь ласка або натисніть /cancel для відміни",
        reply_markup=share_location_kb,
    )
    await state.set_state(StatesLocation.GET_LOCATION)


# Cancellation option
@fill_data.message(Command("cancel"), StateFilter(StatesLocation))
@fill_data.message(F.text.casefold() == "cancel", StateFilter(StatesLocation))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "ви відмовилися ділитися локацією. повертайтеся ще!",
        reply_markup=ReplyKeyboardRemove(),
    )


# Save coordinates, find the city and ask for confirmation
@fill_data.message(StatesLocation.GET_LOCATION, F.location)
async def location_handler(message: Message, state: FSMContext, bot: Bot):
    latitude = message.location.latitude
    longitude = message.location.longitude
    geolocator = Nominatim(user_agent="test_tg_bot")
    location = geolocator.reverse(f"{latitude},{longitude}")
    address = location.raw["address"]
    city = address.get("city", "")
    request = {
        "name": "test_name",
        "description": "test_decs",
        "dangerLevel": 0,
        "coordinates": {"latitude": latitude, "longitude": longitude},
        "accessToken": "string",
    }
    response = requests.post(
        "https://hlp-me-back.onrender.com/local/dangers/create", json=request
    )

    print(response.status_code)
    print(response.json())
    await message.answer(
        f"координати: {latitude}, {longitude}\n" f"місто: {city}",
        reply_markup=ReplyKeyboardRemove(),
    )

    await update_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        collection=collection,
        latitude=latitude,
        longitude=longitude,
    )

    # await collection.update_one(
    #     {"user_id": message.from_user.id},
    #     {"$set": {"latitude": latitude, "longitude": longitude}},
    # )

    await message.answer_location(latitude=latitude, longitude=longitude)
    await bot.send_message(
        ADMIN_ID[0],
        f"user: {message.from_user.mention_html()}\ncoords: {latitude}, {longitude}\ncity: {city}",
        reply_markup=ReplyKeyboardRemove(),
    )


@fill_data.message(StatesLocation.GET_LOCATION)
async def unwanted_location_handler(message: Message, state: FSMContext):
    await message.answer(
        "скористайтеся, будь ласка, кнопкою або натисніть /cancel для відміни",
        reply_markup=ReplyKeyboardRemove(),
    )
