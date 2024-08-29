from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from auth.models import User
from core.database.models import Base
# currencies.models import Currency  # TODO без этого можно обойтись?


class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(128))
    user_uuid: Mapped['User'] = mapped_column(ForeignKey('users.uuid'))
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'))

   # currency: Mapped[Currency] = relationship()

    def __repr__(self):
        return f'Account [#{self.id}]: {self.name}'
