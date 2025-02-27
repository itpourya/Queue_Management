from src.repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.pydantic_models import RegisterFields
from src.pkg.jwt import Security

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)
    
    async def create_user_service(self, user_data: RegisterFields) -> bool:
        if user_data.username == "" or user_data.password == "" or user_data.email == "":
            return False
        user_data.password = Security.get_password_hash(user_data.password)
        status = await self.repo.create(user_data)

        return status