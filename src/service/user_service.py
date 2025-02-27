from src.repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.pydantic_models import RegisterFields, GetUserByUsername
from src.pkg.jwt import Security
from src.models.user_model import User
from typing import Tuple

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)
    
    async def create_user_service(self, user_data: RegisterFields) -> bool:
        if user_data.username == "" or user_data.password == "" or user_data.email == "":
            return False
        user_data.password = Security.get_password_hash(user_data.password)
        status = await self.repo.create(user_data)

        return status

    async def get_user_service(self, user_data: GetUserByUsername) -> Tuple[bool, User|None]:
        if not user_data.username:
            return False, None

        user = self.repo.get(user_input=user_data)

        return True, user[1]