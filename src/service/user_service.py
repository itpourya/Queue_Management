from src.repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.pydantic_models import RegisterFields, GetUserByUsername, LoginFields, Token
from src.pkg.jwt import Security
from src.models.user_model import User
from typing import Tuple
from src.pkg.jwt import Security
from fastapi import status, HTTPException

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

    async def login_user_service(self, user_input: LoginFields) -> Tuple[bool, Token]:
        if not user_input.username or not user_input.password:
            return False, None

        user = await self.repo.get(username=user_input.username)
        if not user[0]:
            return False, None

        if Security.verify_password(user_input.password, user[1].hashed_password):
            token = Security.create_access_token({
                "username": user[1].username,
                "email": user[1].email
            })

            return True, Token(access_token=token, token_type="bearer")

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )