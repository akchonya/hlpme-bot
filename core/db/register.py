from pymongo.collection import Collection


async def is_user_exists(user_id: int, collection: Collection):
    user = await collection.count_documents({"user_id": user_id})
    if user:
        return True
    return False


async def create_user(user_id: int, username: str, collection: Collection) -> None:
    await collection.insert_one(
        {
            "user_id": user_id,
            "username": username,
        }
    )


async def update_user(user_id: int, username: str, collection: Collection) -> None:
    # update 'data' if 'name' exists otherwise insert new document
    collection.find_one_and_update(
        {"user_id": user_id}, {"$set": {"username": username}}, upsert=True
    )
