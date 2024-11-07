from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from departments.models import Department

from auth.models import User
from core.database.models import Base
# currencies.models import Currency  # TODO без этого можно обойтись?


class Person(Base):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    surname: Mapped[str] = mapped_column(String(32))
    role: Mapped[str] = mapped_column(String(32))
    department_id: Mapped['Department'] = mapped_column(ForeignKey('departments.id'))
    user_uuid: Mapped['User'] = mapped_column(ForeignKey('users.uuid'))
    #ПОТОМ УБРАТЬ ЮЗЕР АЙДИ

    def __repr__(self):
        return f'Person [#{self.id}]: {self.name}'
