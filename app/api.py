import logging
from fastapi import APIRouter
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router

api_router = APIRouter()

# Include routers
api_router.include_router(auth_router)
api_router.include_router(user_router)
