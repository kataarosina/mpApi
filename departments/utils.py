from fastapi import HTTPException, status

#from accounts.models import Account
from departments.models import Department
from auth.models import User
from core.database.session import DBSession
from core.exceptions import HTTP404


def get_user_department(db_session: DBSession, user: User, department_id: int) -> Department:
    department = db_session.get(Department, department_id)
    if department is None:
        raise HTTP404(f'Department #{department_id} does not exists.')

    # if account.user_uuid != user.uuid:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You have no access to this resource. (Not your account.)",
    #     )
    return department
