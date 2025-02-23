from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.pydantic_models import RegisterFields
from src.models.user_model import User
import logging
import uuid

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create(self, user_input: RegisterFields) -> bool:
        new_user: User = User(
            id = uuid.uuid4(),
            username = RegisterFields.username,
            email = RegisterFields.email,
            hashed_password = RegisterFields.password
            )        
        try:
            self.session.add(new_user)
            await self.session.commit()
            return True

        except Exception as e:
            logger.error(f"Error in create() Repository: {e}")
            return False


    def get(self):
        pass


    def delete(self):
        pass


    def update(self):
        pass
