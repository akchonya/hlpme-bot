from motor.motor_asyncio import AsyncIOMotorClient
from core.utils.config import DB_URL
from pymongo.collection import Collection


cluster = AsyncIOMotorClient(DB_URL)
collection: Collection = cluster.bot_test_db.users
