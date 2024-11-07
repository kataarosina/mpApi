from uuid import UUID

from pydantic import BaseModel

from core.dtos import Base


class UserCreate(Base):

    username: str
    password: str
    name: str
    surname: str


class User(Base):

    uuid: UUID
    username: str
    hashed_password: bytes
    is_active: bool
    name: str
    surname: str

class UserCreateDTO(BaseModel):
    
    username: str
    hashed_password: bytes
    is_active: bool
    name: str
    surname: str


class Token(BaseModel):
    
    access_token: str
    token_type: str

class TokenData(BaseModel):

    username: str | None = None
