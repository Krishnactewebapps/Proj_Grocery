import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserBase
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import AuthService
from typing import Any

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

user_service = UserService()
auth_service = AuthService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Any:
    user = await auth_service.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials.")
    return user

@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    logger.info(f"Fetching profile for user: {current_user['email']}")
    user = await user_service.get_user_by_email(current_user['email'])
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.put("/me", response_model=UserResponse)
async def update_profile(payload: UserBase, current_user: dict = Depends(get_current_user)):
    logger.info(f"Updating profile for user: {current_user['email']}")
    updated_user = await user_service.update_user_profile(current_user['email'], payload)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or update failed.")
    return updated_user
