import logging
from typing import Optional
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserBase, UserCreate
from app.utils.validation import validate_user_update

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        logger.info(f"Retrieving user by email: {email}")
        user = await self.user_repo.get_by_email(email)
        if not user:
            logger.warning(f"User not found: {email}")
            return None
        return user

    async def create_user(self, user_create: UserCreate) -> Optional[dict]:
        logger.info(f"Creating user: {user_create.email}")
        if await self.user_repo.get_by_email(user_create.email):
            logger.warning(f"User already exists: {user_create.email}")
            return None
        user_data = user_create.dict()
        user = await self.user_repo.create(user_data)
        logger.info(f"User created: {user_create.email}")
        return user

    async def update_user_profile(self, email: str, user_update: UserBase) -> Optional[dict]:
        logger.info(f"Updating user profile for: {email}")
        # Validate update fields
        validation_result = validate_user_update(user_update)
        if not validation_result['valid']:
            logger.warning(f"Validation failed for user update: {validation_result['error']}")
            return None
        updated_user = await self.user_repo.update_by_email(email, user_update.dict(exclude_unset=True))
        if not updated_user:
            logger.warning(f"User not found or update failed: {email}")
            return None
        logger.info(f"User profile updated: {email}")
        return updated_user
