import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from fastapi import FastAPI

logger = logging.getLogger(__name__)

MONGO_URI = "mongodb://localhost:27017"  # You may want to load this from environment variables
MONGO_DB_NAME = "mydatabase"  # You may want to load this from environment variables

mongo_client: Optional[AsyncIOMotorClient] = None
mongo_db: Optional[AsyncIOMotorDatabase] = None

def get_mongo_db() -> AsyncIOMotorDatabase:
    global mongo_db
    if not mongo_db:
        raise RuntimeError("MongoDB is not connected.")
    return mongo_db

async def connect_to_mongo():
    global mongo_client, mongo_db
    if not mongo_client:
        logger.info("Connecting to MongoDB at %s", MONGO_URI)
        mongo_client = AsyncIOMotorClient(MONGO_URI)
        mongo_db = mongo_client[MONGO_DB_NAME]
        logger.info("MongoDB connection established.")

async def close_mongo_connection():
    global mongo_client, mongo_db
    if mongo_client:
        logger.info("Closing MongoDB connection.")
        mongo_client.close()
        mongo_client = None
        mongo_db = None
        logger.info("MongoDB connection closed.")
