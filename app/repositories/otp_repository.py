import logging
from typing import Optional, Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorCollection
from app.db import get_mongo_db

logger = logging.getLogger(__name__)

class OTPRepository:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_mongo_db()["otps"]

    async def save_otp(self, email: str, otp: str, expires_at: datetime) -> None:
        logger.info(f"Saving OTP for {email}")
        await self.collection.update_one(
            {"email": email},
            {"$set": {"otp": otp, "expires_at": expires_at}},
            upsert=True
        )

    async def get_otp(self, email: str) -> Optional[Dict[str, Any]]:
        logger.info(f"Fetching OTP for {email}")
        otp_record = await self.collection.find_one({"email": email})
        if otp_record:
            otp_record["expires_at"] = otp_record["expires_at"] if isinstance(otp_record["expires_at"], datetime) else datetime.strptime(otp_record["expires_at"], "%Y-%m-%dT%H:%M:%S.%f")
        return otp_record

    async def delete_otp(self, email: str) -> None:
        logger.info(f"Deleting OTP for {email}")
        await self.collection.delete_one({"email": email})

    async def count_recent_otps(self, email: str, window_seconds: int = 300) -> int:
        """
        Count OTPs generated for an email in the last `window_seconds` seconds (default 5 minutes).
        Used for rate limiting.
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)
        count = await self.collection.count_documents({
            "email": email,
            "expires_at": {"$gte": window_start}
        })
        return count
