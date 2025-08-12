import logging
from fastapi import FastAPI
from app.db import connect_to_mongo, close_mongo_connection
from app.api import api_router

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI MongoDB Microservice")

# Include API routers
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up and connecting to MongoDB...")
    await connect_to_mongo()
    logger.info("Connected to MongoDB.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down and closing MongoDB connection...")
    await close_mongo_connection()
    logger.info("MongoDB connection closed.")
