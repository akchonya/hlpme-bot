from datetime import datetime

import requests
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from geopy.geocoders import Nominatim

from core.keyboards.needhelp import confirm_help_ikb, share_location_kb
from core.utils.states_location import StatesNeedHelp

i_need_help_router = Router()


@i_need_help_router.message(Command("i_need_help"))
async def need_help_handler(message: Message, state: FSMContext):
    await message.answer(
        "якщо ви потребуєте допомоги - введіть запит.\n\n"
        "зауважте, що разом із запитом передасться і ваша поточна інформація."
        "тому, якщо ви ще не заповнили додаткові дані - скористайтеся /fill_data\n\n"
        "натисніть /cancel для відміни\n\n"
        "будь ласка, зауважте, що тут подати запит можна виключно з мобільного пристрою",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(StatesNeedHelp.GET_CAPTION)


# Cancellation option
@i_need_help_router.message(Command("cancel"), StateFilter(StatesNeedHelp))
@i_need_help_router.message(F.text.casefold() == "cancel", StateFilter(StatesNeedHelp))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "створення запиту відмінено!",
        reply_markup=ReplyKeyboardRemove(),
    )


@i_need_help_router.message(StatesNeedHelp.GET_CAPTION, F.text)
async def get_help_caption_handler(message: Message, state: FSMContext):
    await state.update_data(caption=message.text)
    await message.answer(
        "опишіть свою проблему або натисніть /skip якщо не хочете надавати підробиць"
    )
    await state.set_state(StatesNeedHelp.GET_DESCRIPTION)


@i_need_help_router.message(StatesNeedHelp.GET_CAPTION)
async def unwanted_help_caption_handler(message: Message):
    await message.answer(
        "введіть текстом або пропустіть командою /skip\n.якщо хочете відмінити - /cancel"
    )


@i_need_help_router.message(StatesNeedHelp.GET_DESCRIPTION, Command("skip"))
async def skip_description(message: Message, state: FSMContext):
    await state.update_data(description="деталі відсутні.")
    await message.answer("добре, поділіться локацією:", reply_markup=share_location_kb)
    await state.set_state(StatesNeedHelp.GET_LOCATION)


@i_need_help_router.message(StatesNeedHelp.GET_DESCRIPTION, F.text)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("добре, поділіться локацією:", reply_markup=share_location_kb)
    await state.set_state(StatesNeedHelp.GET_LOCATION)


@i_need_help_router.message(StatesNeedHelp.GET_DESCRIPTION)
async def unwanted_description(message: Message):
    await message.answer("введіть коректні текстові дані")


@i_need_help_router.message(StatesNeedHelp.GET_LOCATION, F.location)
async def get_location(message: Message, state: FSMContext):
    await state.update_data(latitude=message.location.latitude)
    await state.update_data(longitude=message.location.longitude)
    await message.answer(
        "записано. вкажіть день, на який вам потрібна допомога у форматі дд-мм-рррр:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(StatesNeedHelp.GET_DATE)


@i_need_help_router.message(StatesNeedHelp.GET_LOCATION)
async def unwanted_location(message: Message, state: FSMContext):
    await message.reply(
        "будь ласка, скористайтеся клавіатурою для подання локації "
        "або натисніть /cancel для відміни.\n\n"
        "якщо ви з пристрою, який не підтримує цю функцію - спробуйте "
        "подати запит на нашому сайті {лінк_на_сайт}"
    )


@i_need_help_router.message(StatesNeedHelp.GET_DATE, F.text)
async def get_date_handler(message: Message, state: FSMContext):
    date_text = message.text
    try:
        # Attempt to parse the input string as a date
        date_object = str(datetime.strptime(date_text, "%d-%m-%Y"))
    except ValueError:
        await message.answer(
            "введіть дату у форматі дд-мм-рррр", reply_markup=ReplyKeyboardRemove()
        )
        return
    await state.update_data(date=date_object)

    context_data = await state.get_data()
    caption = context_data.get("caption")
    description = context_data.get("description")
    date = context_data.get("date")
    latitude = context_data.get("latitude")
    longitude = context_data.get("longitude")

    geolocator = Nominatim(user_agent="test_tg_bot")
    location = geolocator.reverse(f"{latitude},{longitude}")
    address = location.raw["address"]
    city = address.get("city", "")

    await message.answer(
        "записано! перевірте, будь ласка, дані:\n"
        f"проблема: {caption}\n"
        f"опис: {description}\n"
        f"місто: {city}\n"
        f"дата: {date}",
        reply_markup=confirm_help_ikb,
    )

    await state.set_state(StatesNeedHelp.CHECK)


@i_need_help_router.callback_query(StatesNeedHelp.CHECK)
async def check_handler(callback: CallbackQuery, state: FSMContext):
    action = callback.data

    if action == "help_confirm":
        context = await state.get_data()
        caption = context.get("caption")
        description = context.get("description")
        date_time = context.get("date")
        latitude = context.get("latitude")
        longitude = context.get("longitude")

        request = {
            "user_id": callback.from_user.id,
            "name": caption,
            "description": description,
            "date_time": date_time,
            "coordinates": {"latitude": latitude, "longitude": longitude},
            "accessToken": "string",
        }
        response = requests.post(
            "https://hlp-me-back.onrender.com/local/dangers/create", json=request
        )

        await callback.message.answer(
            "запит додано!", reply_markup=ReplyKeyboardRemove()
        )
        print(response.status_code)
        print(response.json())

        await state.clear()
        await callback.answer()

    elif action == "help_decline":
        await callback.message.answer(
            "відмінено. можете спробувати ще раз натиснувши /i_need_help",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
        await callback.answer()


# @i_need_help_router.callback_query()
# async def unwanted_callback_handler(callback: CallbackQuery):
#     await callback.answer()
