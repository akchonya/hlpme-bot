from motor.motor_asyncio import AsyncIOMotorClient
from core.utils.config import DB_URL

cluster = AsyncIOMotorClient(DB_URL)
collection = cluster.bot_test_db.users
