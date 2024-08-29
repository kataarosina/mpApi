from fastapi import HTTPException, status

from accounts.models import Account
from auth.models import User
from core.database.session import DBSession
from core.exceptions import HTTP404


def get_user_account(db_session: DBSession, user: User, account_id: int) -> Account:
    account = db_session.get(Account, account_id)
    if account is None:
        raise HTTP404(f'Account #{account_id} does not exists.')

    if account.user_uuid != user.uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have no access to this resource. (Not your account.)",
        )
    return account
