import requests

from email_validator import validate_email, EmailNotValidError
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from core.utils.states_fill import StatesFill
from core.keyboards.filldata import share_phone_kb, confirm_fill_ikb

filldata_router = Router()


# Ask user for their location
@filldata_router.message(Command("fill_data"))
async def fill_data_handler(message: Message, state: FSMContext):
    await message.answer(
        "введіть повне ім'я у форматі Прізвище Ім'я\nякщо хочете відмінити дію -> /cancel",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(StatesFill.GET_FULLNAME)


# Cancellation option
@filldata_router.message(Command("cancel"), StateFilter(StatesFill))
@filldata_router.message(F.text.casefold() == "cancel", StateFilter(StatesFill))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "відмінено. повертайтеся ще!",
        reply_markup=ReplyKeyboardRemove(),
    )


# Save coordinates, find the city and ask for confirmation
@filldata_router.message(
    StatesFill.GET_FULLNAME,
    F.text.regexp(
        "^[А-ЯІЇЄа-яіїє][А-ЯІЇЄа-яіїє']*\s[А-ЯІЇЄа-яіїє][А-ЯІЇЄа-яіїє']*$"
    ),  # re to check whether the full name is in the right format
)
async def get_fullname(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(full_name=message.text)
    await message.answer(
        "ім'я записано. введіть email або скористайтеся /cancel для відміни"
    )
    await state.set_state(StatesFill.GET_EMAIL)


@filldata_router.message(StatesFill.GET_FULLNAME)
async def unwanted_fm_handler(message: Message):
    await message.answer(
        "введіть дані у форматі Прізвище Ім'я або /cancel для відміни",
        parse_mode="HTML",
    )


@filldata_router.message(StatesFill.GET_EMAIL, F.text)
async def get_email(message: Message, state: FSMContext):
    email = message.text

    # Check email
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        email = emailinfo.normalized

    # Ask for email again on False
    except EmailNotValidError:
        await message.answer(
            "введіть коректний email або натисніть /cancel для відміни"
        )

        return

    await state.update_data(email=email)
    await message.answer(
        "email записано. поділіться номером телефону за допомогою кнопки нижче",
        reply_markup=share_phone_kb,
    )
    await state.set_state(StatesFill.GET_PHONE)


@filldata_router.message(StatesFill.GET_PHONE, F.contact)
async def get_phone_handler(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    context_data = await state.get_data()
    full_name = context_data.get("full_name")
    email = context_data.get("email")
    phone_number = context_data.get("phone_number")
    await message.answer(
        "записано! перевірте, будь ласка, дані: \n"
        f"повне ім'я: {full_name}\n"
        f"email: {email}\n"
        f"номер телефону: {phone_number}",
        reply_markup=confirm_fill_ikb,
    )
    await state.set_state(StatesFill.CHECK)


@filldata_router.message(StatesFill.GET_PHONE)
async def unwanted_phone_handler(message: Message, state: FSMContext):
    await message.answer(
        "будь ласка, поділіться номером телефону за допомогою кнопки нижче або скористайтеся /cancel для відміни",
        reply_markup=share_phone_kb,
    )


@filldata_router.callback_query(StatesFill.CHECK)
async def check_handler(callback: CallbackQuery, state: FSMContext):
    action = callback.data

    if action == "confirm":
        context_data = await state.get_data()
        full_name = context_data.get("full_name")
        email = context_data.get("email")
        phone_number = context_data.get("phone_number")
        await callback.message.answer("записано!", reply_markup=ReplyKeyboardRemove())

        request = {
            "full_name": full_name,
            "email": email,
            "phone_number": phone_number,
            "accessToken": "string",
        }
        response = requests.post(
            "https://hlp-me-back.onrender.com/bot/create/user", json=request
        )

        print(response.status_code)
        print(response.json())

        await state.clear()
        await callback.answer()

    elif action == "decline":
        await callback.message.answer(
            "відмінено. можете спробувати ще раз натиснувши /fill_data",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
        await callback.answer()


# @filldata_router.callback_query()
# async def unwanted_callback_handler(callback: CallbackQuery):
#     await callback.answer()
