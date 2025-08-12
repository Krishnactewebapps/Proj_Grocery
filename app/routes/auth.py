import logging
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, constr
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

auth_service = AuthService()
user_service = UserService()

class RegisterRequest(UserCreate):
    pass

class LoginRequest(UserLogin):
    pass

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(payload: RegisterRequest):
    logger.info(f"Registering user: {payload.email}")
    user = await user_service.create_user(payload)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists or invalid data.")
    return user

@router.post("/login", response_model=TokenResponse)
async def login_user(payload: LoginRequest):
    logger.info(f"User login attempt: {payload.email}")
    token = await auth_service.authenticate_user(payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return {"access_token": token, "token_type": "bearer"}
