import requests
from aiogram import Router, html, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from core.keyboards.delete_help import delete_help, confirm_delete_ikb
from core.utils.states_delete import StatesDelete

profile_router = Router()

user_ads = {}
user_ads_names = {}
user_ads_names_delete = {}


@profile_router.message(Command("profile"))
async def profile_handler(message: types.Message):
    user_id = message.from_user.id
    response = requests.get(f"https://hlp-me-back.onrender.com/user/{user_id}")
    response_status = int(response.status_code)
    print(response_status)
    if response_status == 500:
        await message.answer(
            "наразі сервіс недоступний, перепрошуємо за незручності 😩\nспробуйте пізніше"
        )
        return
    response = response.json()
    print(response)
    profile = (
        f"{html.bold('ваш профіль:')} \n👤 ім'я: {response['full_name']}\n🖥 username:"
        f" {response['username']}\n📧 email: {response['email']}\n📞 номер телефону:"
        f" {response['phone_number']}\n\nякщо хочете {html.underline('оновити дані')} -"
        " /fill_data\n\n"
    )

    helps_responce = requests.get(
        f"https://hlp-me-back.onrender.com/local/dangers/my/{user_id}"
    )

    helps_responce_status = int(helps_responce.status_code)
    print(helps_responce_status)
    if helps_responce_status == 500:
        await message.answer(
            "наразі сервіс недоступний, перепрошуємо за незручності 😩\nспробуйте пізніше"
        )
        return

    helps_responce = helps_responce.json()
    print(helps_responce)
    user_ads[user_id] = helps_responce

    if len(helps_responce) == 0:
        helps = "❕ ви поки не створювали запити на допомогу.\nдля цього скористайтеся /i_need_help"
    else:
        helps = f"🟢 {html.bold('ваші активні запити на допомогу')}:\n"
        for i in range(len(helps_responce)):
            help = helps_responce[i]
            helps += f"{i+1}. {help['name']}\n"
        helps += "\n✏️ ви можете видалити запит за допомогою команди /delete"
    await message.answer(profile + helps, reply_markup=ReplyKeyboardRemove())


@profile_router.message(Command("delete"))
async def delete_help_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # helps_responce = requests.get(
    #     f"https://hlp-me-back.onrender.com/local/dangers/my/{user_id}"
    # )
    # helps_responce_status = int(helps_responce.status_code)
    # print(helps_responce_status)
    # if helps_responce_status == 500:
    #     await message.answer(
    #         "наразі сервіс недоступний, перепрошуємо за незручності 😩\nспробуйте пізніше"
    #     )
    #     return

    # helps_responce = helps_responce.json()
    # print(helps_responce)

    helps_responce = user_ads[user_id]

    if not len(helps_responce):
        await message.answer(
            "❕ ви ще не створили запитів на допомогу.",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        helps = []
        for help in helps_responce:
            helps.append(help["name"])

        user_ads_names[user_id] = helps

        kb = await delete_help(names=helps)
        await message.answer("✏️ оберіть з переліку нижче або /cancel", reply_markup=kb)
        await state.set_state(StatesDelete.GET_HELP)


# Cancellation option
@profile_router.message(Command("cancel"), StateFilter(StatesDelete))
@profile_router.message(F.text.casefold() == "cancel", StateFilter(StatesDelete))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "🔴 відмінено. повертайтеся ще!",
        reply_markup=ReplyKeyboardRemove(),
    )


@profile_router.message(StatesDelete.GET_HELP)
async def get_help_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text not in user_ads_names[user_id]:
        await message.answer("✏️ оберіть зі списку або відмініть /cancel")
    else:
        await message.answer(
            f"{html.bold('📝 перевірте дані')}:\nви видаляєте {html.underline(message.text)}\nпідтверджуєте?",
            reply_markup=confirm_delete_ikb,
        )
        await state.update_data(name=message.text)
        print("TO DELETE CHECK")
        user_ads_names_delete[user_id] = message.text
    await state.set_state(StatesDelete.CONFIRM)


@profile_router.callback_query(StatesDelete.CONFIRM)
async def confirm_delete_handler(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    print(user_ads_names_delete[callback.from_user.id])
    if action == "delete_confirm":
        context_data = await state.get_data()
        name = context_data.get("name")

        my_user_ads = user_ads[callback.from_user.id]
        for item in my_user_ads:
            if item["name"] == name:
                id = item["_id"]
        response = requests.delete(
            f"https://hlp-me-back.onrender.com/local/dangers/delete/{id}"
        )
        print(response.status_code)
        print(response.json())
        await callback.message.answer(
            "✅ успішно видалено", reply_markup=ReplyKeyboardRemove()
        )
        await callback.answer()

    elif action == "delete_decline":
        await callback.message.answer(
            "🔴 відмінено. можете спробувати ще раз натиснувши /delete",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
        await callback.answer()
