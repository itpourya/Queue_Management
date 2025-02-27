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


    def get(self, user_input: GetUserByUsername) -> User | bool:
        query = sqlalchemy.select(User).where(User.username == user_input.username)

        async with self.session as session:
            user = session.scalar(query)

            if not user.username:
                logger.info(f"Repository: User {user_input} Not Found")
                return False

            return user


    def delete(self):
        pass


    def update(self):
        pass
