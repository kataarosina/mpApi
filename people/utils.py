from fastapi import HTTPException, status

#from accounts.models import Account
from people.models import Person
from auth.models import User
from core.database.session import DBSession
from core.exceptions import HTTP404


def get_user_person(db_session: DBSession, user: User, person_id: int) -> Person:
    person = db_session.get(Person, person_id)
    if person is None:
        raise HTTP404(f'Person #{person_id} does not exists.')

    # if account.user_uuid != user.uuid:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You have no access to this resource. (Not your account.)",
    #     )
    return person
