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


async def update_user(
    user_id: int,
    username: str,
    collection: Collection,
    latitude="not_shared",
    longitude="not_shared",
    city="not_shared",
) -> None:
    # update data if "user_id" exists otherwise insert new document
    collection.find_one_and_update(
        {"user_id": user_id},
        {
            "$set": {
                "username": username,
                "latitude": latitude,
                "longitude": longitude,
                "city": city,
            }
        },
        upsert=True,
    )
