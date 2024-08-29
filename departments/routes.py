from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy import select

from core.database.session import DBSession
from core.database.session import create_db_session

from departments.dtos import  DepartmentDTO, DepartmentCreateDTO
from departments.models import Department
from departments.utils import get_user_department


#from accounts.models import Account
#from accounts.dtos import AccountDTO, AccountCreateDTO
#from accounts.utils import get_user_account
from auth.models import User
from auth.utils import get_current_active_user

departments_router = APIRouter(
    prefix='/departments',
    tags=['departments'],
    responses={404: {'description': 'Not found'}},

)


@departments_router.get('/', response_model=list[DepartmentDTO])
async def get_departments(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db_session: DBSession = Depends(create_db_session)
) -> list[Department]:
    #stmt = select(Department).where(Department.user_uuid == current_user.uuid)
    #user_accounts = db_session.scalars(stmt).all()
    smth = select(Department)
    user_departments = db_session.scalars(smth).all()
    return user_departments
#ПЕРЕИМЕНОВАТЬ ПЕРЕМЕННЫЕ ВЫШЕ И ПЕРЕПИСАТЬ ЗАПРОС

@departments_router.get('/{department_id}', response_model=DepartmentDTO)
async def get_department(
        current_user: Annotated[User, Depends(get_current_active_user)],
       department_id: int, db_session: DBSession = Depends(create_db_session)
) -> Department:
    department = get_user_department(db_session, current_user, department_id)
    return department
#ЗДЕСЬ УБРАТЬ ЮЗЕРА ИЗ ПАРАМЕТРОВ

@departments_router.post('/')
async def create_department(
    current_user: Annotated[User, Depends(get_current_active_user)],
    dto_data: DepartmentCreateDTO,
    db_session: DBSession = Depends(create_db_session)
) -> dict:
    data = dto_data.model_dump()
    data['user_uuid'] = current_user.uuid
    try:
        new_department = Department(**data)
        db_session.add(new_department)
    except Exception as e:
        db_session.rollback()
        print(e)
        return {'status': 'ERROR', 'message': 'Something went wrong!'}
    else:
        db_session.commit()
    return {'status': 'OK', 'message': f'New department for user {current_user.username} created!'}
