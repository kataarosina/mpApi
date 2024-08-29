from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy import select

from core.database.session import DBSession
from core.database.session import create_db_session

from accounts.models import Account
from accounts.dtos import AccountDTO, AccountCreateDTO
from accounts.utils import get_user_account
from auth.models import User
from auth.utils import get_current_active_user

accounts_router = APIRouter(
    prefix='/accounts',
    tags=['accounts'],
    responses={404: {'description': 'Not found'}},

)


@accounts_router.get('/', response_model=list[AccountDTO])
async def get_accounts(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db_session: DBSession = Depends(create_db_session)
) -> list[Account]:
    stmt = select(Account).where(Account.user_uuid == current_user.uuid)
    user_accounts = db_session.scalars(stmt).all()
    return user_accounts


@accounts_router.get('/{account_id}', response_model=AccountDTO)
async def get_account(
        current_user: Annotated[User, Depends(get_current_active_user)],
        account_id: int, db_session: DBSession = Depends(create_db_session)
) -> Account:
    account = get_user_account(db_session, current_user, account_id)
    return account


@accounts_router.post('/')
async def create_account(
    current_user: Annotated[User, Depends(get_current_active_user)],
    dto_data: AccountCreateDTO,
    db_session: DBSession = Depends(create_db_session)
) -> dict:
    data = dto_data.model_dump()
    data['user_uuid'] = current_user.uuid
    try:
        new_account = Account(**data)
        db_session.add(new_account)
    except Exception as e:
        db_session.rollback()
        print(e)
        return {'status': 'ERROR', 'message': 'Something went wrong!'}
    else:
        db_session.commit()
    return {'status': 'OK', 'message': f'New account for user {current_user.username} created!'}
