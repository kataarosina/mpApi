from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from core.database.models import Base


class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(unique=False, nullable=True)
    surname: Mapped[str] = mapped_column(unique=False, nullable=True)

    def __repr__(self):
        return f'User: {self.username}. Active: {self.is_active}'
