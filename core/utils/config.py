from os import getenv
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
DORM_CHAT_ID = getenv("DORM_CHAT_ID")
WEBHOOK_SECRET = getenv("WEBHOOK_SECRET")
BASE_WEBHOOK_URL = getenv("BASE_WEBHOOK_URL")
WEB_SERVER_HOST = getenv("WEB_SERVER_HOST")
ADMIN_ID = getenv("ADMIN_ID")
ADMIN_ID = list(map(int, ADMIN_ID.split(", ")))
DB_URL = getenv("DB_URL")
WEB_SERVER_PORT = getenv("WEB_SERVER_PORT")
