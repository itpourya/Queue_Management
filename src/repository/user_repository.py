from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.pydantic_models import RegisterFields, GetUserByUsername
from src.models.user_model import User
from typing import Tuple
import logging
import uuid
import sqlalchemy as sq

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create(self, user_input: RegisterFields) -> bool:
        new_user = User()
        new_user.id = uuid.uuid4()
        new_user.username = user_input.username 
        new_user.hashed_password = user_input.password
        new_user.email = user_input.email
        
        try:
            async with self.session:
                self.session.add(new_user)
                await self.session.commit()
                logger.info(f"Repository: User {new_user} Created")
                return True

        except Exception as e:
            logger.error(f"Error in create() Repository: {e}")
            return False


    async def get(self, username: str) -> Tuple[bool, User]:
        query = sq.select(User).where(User.username == username)

        try:
            async with self.session as session:
                user = await session.scalar(query)

            if user is None:
                logger.info(f"Repository: User {username} Not Found")
                return False, None
        except Exception as e:
            logger.error(f"Error in get() Repository: {e}")
            return False, None

        return True, user


    def delete(self):
        pass


    def update(self):
        pass
