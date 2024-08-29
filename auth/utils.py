from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select

from auth.dtos import UserCreate
from auth.exceptions import credentials_validate_exception
from auth.models import User
from core.config import Config
from core.database.session import DBSession
from core.database.session import create_db_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class PasswordManager:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)


def create_user(data: UserCreate) -> User | None:
    with DBSession() as db_session:
        try:
            user = User(
                username=data.username,
                hashed_password=PasswordManager.get_password_hash(data.password)
            )
            db_session.add(user)
        except Exception as e:
            db_session.rollback()
            print(e)
        else:
            db_session.commit()
            return user


def get_user(db_session: DBSession, username: str) -> User:
    stmt = select(User).where(User.username == username)
    user = db_session.execute(stmt).scalar()
    return user


def authenticate(db_session: DBSession, username: str, password) -> User | bool:
    stmt = select(User).where(User.username == username)
    user = db_session.execute(stmt).scalar()
    if not user:
        return False
    if not PasswordManager.verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(payload: dict, expires_delta: timedelta | None = None) -> str:
    payload = payload.copy()
    if expires_delta is None:
        expire_data = datetime.now() + timedelta(minutes=Config.JWT_ACCESS_TOKEN_TTL_MINUTES)
    else:
        expire_data = datetime.now() + expires_delta

    payload.update({'exp': expire_data})
    encoded_jwt = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_HASHING_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db_session: DBSession = Depends(create_db_session)
):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_HASHING_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_validate_exception
    except jwt.PyJWTError:
        raise credentials_validate_exception
    user = get_user(db_session, username=username)
    if user is None:
        raise credentials_validate_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
