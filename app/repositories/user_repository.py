import logging
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from app.db import get_mongo_db

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_mongo_db()["users"]

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        user = await self.collection.find_one({"email": email})
        if user:
            user["id"] = str(user["_id"])
            user.pop("_id", None)
        return user

    async def create(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = await self.collection.insert_one(user_data)
        if result.inserted_id:
            user = await self.collection.find_one({"_id": result.inserted_id})
            user["id"] = str(user["_id"])
            user.pop("_id", None)
            return user
        return None

    async def update_by_email(self, email: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = await self.collection.find_one_and_update(
            {"email": email},
            {"$set": update_data},
            return_document=True
        )
        if result:
            result["id"] = str(result["_id"])
            result.pop("_id", None)
            return result
        return None

    async def delete_by_email(self, email: str) -> bool:
        result = await self.collection.delete_one({"email": email})
        return result.deleted_count > 0
