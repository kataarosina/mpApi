from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy import select

from core.database.session import DBSession
from core.database.session import create_db_session

from people.dtos import  PersonDTO, PersonCreateDTO
from people.models import Person
from people.utils import get_user_person


#from accounts.models import Account
#from accounts.dtos import AccountDTO, AccountCreateDTO
#from accounts.utils import get_user_account
from auth.models import User
from auth.utils import get_current_active_user

people_router = APIRouter(
    prefix='/people',
    tags=['people'],
    responses={404: {'description': 'Not found'}},

)


@people_router.get('/', response_model=list[PersonDTO])
async def get_people(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db_session: DBSession = Depends(create_db_session)
) -> list[Person]:
    #stmt = select(Department).where(Department.user_uuid == current_user.uuid)
    #user_accounts = db_session.scalars(stmt).all()
    smth = select(Person)
    user_people = db_session.scalars(smth).all()
    return user_people
#ПЕРЕИМЕНОВАТЬ ПЕРЕМЕННЫЕ ВЫШЕ И ПЕРЕПИСАТЬ ЗАПРОС

@people_router.get('/{person_id}', response_model=PersonDTO)
async def get_person(
        current_user: Annotated[User, Depends(get_current_active_user)],
        person_id: int, db_session: DBSession = Depends(create_db_session)
) -> Person:
    person = get_user_person(db_session, current_user, person_id)
    return person
#ЗДЕСЬ УБРАТЬ ЮЗЕРА ИЗ ПАРАМЕТРОВ

@people_router.post('/')
async def create_person(
    current_user: Annotated[User, Depends(get_current_active_user)],
    dto_data: PersonCreateDTO,
    db_session: DBSession = Depends(create_db_session)
) -> dict:
    data = dto_data.model_dump()
    data['user_uuid'] = current_user.uuid
    try:
        new_person = Person(**data)
        db_session.add(new_person)
    except Exception as e:
        db_session.rollback()
        print(e)
        return {'status': 'ERROR', 'message': 'Something went wrong!'}
    else:
        db_session.commit()
    return {'status': 'OK', 'message': f'New person for user {current_user.username} created!'}
