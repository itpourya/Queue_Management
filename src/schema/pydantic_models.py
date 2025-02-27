from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    id: UUID
    email: str

class RegisterFields(BaseModel):
    username: str
    email: str
    password: str

class GetUserByUsername(BaseModel):
    username: str

class JWTPayload(BaseModel):
    username: str
    email: str
    id: str
    exp: int