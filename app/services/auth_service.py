import logging
import random
import string
from datetime import datetime, timedelta
from typing import Optional

from app.repositories.user_repository import UserRepository
from app.repositories.otp_repository import OTPRepository
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.otp_repo = OTPRepository()
        self.rate_limiter = RateLimiter()

    async def register_user(self, user_create):
        logger.info(f"Attempting to register user: {user_create.email}")
        if await self.user_repo.get_by_email(user_create.email):
            logger.warning(f"Registration failed: User already exists: {user_create.email}")
            return None
        hashed_pwd = hash_password(user_create.password)
        user_data = user_create.dict()
        user_data['password'] = hashed_pwd
        user = await self.user_repo.create(user_data)
        logger.info(f"User registered successfully: {user_create.email}")
        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[str]:
        logger.info(f"Authenticating user: {email}")
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user['password']):
            logger.warning(f"Authentication failed for user: {email}")
            return None
        token = create_access_token({"sub": user['email']})
        logger.info(f"Authentication successful for user: {email}")
        return token

    async def generate_otp(self, email: str) -> Optional[str]:
        logger.info(f"Generating OTP for: {email}")
        if not await self.user_repo.get_by_email(email):
            logger.warning(f"OTP generation failed: User not found: {email}")
            return None
        if not self.rate_limiter.allow(email):
            logger.warning(f"OTP generation rate limit exceeded for: {email}")
            return None
        otp = ''.join(random.choices(string.digits, k=6))
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        await self.otp_repo.save_otp(email, otp, expires_at)
        logger.info(f"OTP generated for {email}: {otp}")
        return otp

    async def verify_otp(self, email: str, otp: str) -> bool:
        logger.info(f"Verifying OTP for: {email}")
        otp_record = await self.otp_repo.get_otp(email)
        if not otp_record:
            logger.warning(f"OTP verification failed: No OTP found for {email}")
            return False
        if otp_record['otp'] != otp:
            logger.warning(f"OTP verification failed: Incorrect OTP for {email}")
            return False
        if datetime.utcnow() > otp_record['expires_at']:
            logger.warning(f"OTP verification failed: OTP expired for {email}")
            return False
        await self.otp_repo.delete_otp(email)
        logger.info(f"OTP verified successfully for {email}")
        return True

    async def get_user_from_token(self, token: str):
        # This function should decode the token and fetch the user
        from app.utils.security import decode_access_token
        payload = decode_access_token(token)
        if not payload or 'sub' not in payload:
            logger.warning("Token decoding failed or invalid payload.")
            return None
        user = await self.user_repo.get_by_email(payload['sub'])
        return user
