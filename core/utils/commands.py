from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


user_commands = [
    BotCommand(command="start", description="розпочати роботу"),
    BotCommand(command="fill_data", description="заповнити дані"),
    BotCommand(command="i_need_help", description="подати запит на допомогу"),
    BotCommand(command="active_helps", description="переглянути активні запити"),
    BotCommand(command="profile", description="ваш профіль"),
]


async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, BotCommandScopeDefault())
