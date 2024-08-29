from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from auth.models import User
from core.database.models import Base
# currencies.models import Currency  # TODO без этого можно обойтись?

#     val id: Int,
#     val name: String?,
#     val description: String?,
#     val imageLink: String?,
#     val quantityOfWorkers: Int?,
#     //val workers: List<String>?


class Department(Base):
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(128))
    imageLink: Mapped[str] = mapped_column(String(128))
    quantityOfWorkers: Mapped[int] = mapped_column(Integer)
    user_uuid: Mapped['User'] = mapped_column(ForeignKey('users.uuid'))

    #currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'))

    # currency: Mapped[Currency] = relationship()
    #ПОТОМ УБРАТЬ ЮЗЕР АЙДИ

    def __repr__(self):
        return f'Department [#{self.id}]: {self.name}'
