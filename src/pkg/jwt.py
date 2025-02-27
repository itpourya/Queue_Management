from datetime import timedelta, timezone, datetime
from typing import Annotated
from uuid import UUID
import jwt
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from passlib.context import CryptContext
from src.schema.pydantic_models import JWTPayload

SECRET_KEY = "SECRET"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Security:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(auth_token: Annotated[str, Header()]) -> JWTPayload:
        jwt_token = auth_token
        if not jwt_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="auth header not found.",
            )
        try:
            token_data = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])

            if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except jwt.exceptions.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return JWTPayload(**token_data)