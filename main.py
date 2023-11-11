"""
This example shows how to use webhook on behind of any reverse proxy (nginx, traefik, ingress etc.)
"""
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from core.utils.commands import set_commands
from core.handlers.start import start_router
from core.handlers.profile import profile_router
from core.handlers.fill_data import filldata_router
from core.handlers.help_commands import i_need_help_router
from core.handlers.register import register_router
from core.utils.config import (
    BASE_WEBHOOK_URL,
    BOT_TOKEN,
    WEB_SERVER_HOST,
    WEB_SERVER_PORT,
    WEBHOOK_SECRET,
)


# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = "/webhook"


async def on_startup(bot: Bot) -> None:
    await set_commands(bot)
    # If you have a self-signed SSL certificate, then you will need to send a public
    # certificate to Telegram
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET,
        allowed_updates=["message", "callback_query"],
    )


def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_routers(
        start_router,
        profile_router,
        filldata_router,
        i_need_help_router,
        register_router,
    )

    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
