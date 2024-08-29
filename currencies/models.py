from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from core.database.models import Base


class Currency(Base):
    __tablename__ = 'currencies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    symbol: Mapped[str] = mapped_column(String(8), unique=True)
    code: Mapped[str] = mapped_column(String(8), unique=True)

    def __repr__(self):
        return f'Currency [#{self.id}]: {self.name}'
