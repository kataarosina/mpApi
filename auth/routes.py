from datetime import timedelta
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from auth.dtos import Token
from auth.exceptions import invalid_credentials_exception
from auth.utils import authenticate, create_access_token, get_current_active_user
from auth.dtos import User
from core.database.session import DBSession, create_db_session
from core.config import Config

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {'description': 'Not found'}},
)


# Аннотации важны в FastAPI!
@router.post("/token")
async def login_for_access_token(
        # Важно использовать Annotated, без него в механизмах FastAPI что-то не будет работать.
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db_session: DBSession = Depends(create_db_session)) -> Token:
    user = authenticate(db_session, form_data.username, form_data.password)
    if not user:
        # Отловится декоратором и грамотно передастся внятным http ответом? В данном случае python-эксепшен
        #  превратится в 401 ответ.
        raise invalid_credentials_exception
    access_token_expires = timedelta(minutes=Config.JWT_ACCESS_TOKEN_TTL_MINUTES)
    access_token = create_access_token(
        payload={"sub": user.username, "sub_uuid": str(user.uuid)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    # Depends запрашивает токен используя OAuth2PasswordBearer из заголовков запроса.
    # Если токена нет, пользователь будет отправлен на роут выше (tokenUrl="/auth/token").
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
