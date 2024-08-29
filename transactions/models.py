from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from accounts.models import Account
from core.database.models import Base


class TransactionType(Base):
    __tablename__ = 'transactions_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    categories: Mapped[list['TransactionCategory']] = relationship(back_populates='type')

    def __repr__(self):
        return f'Type [#{self.id}]: {self.name}'


class TransactionCategory(Base):
    __tablename__ = 'transactions_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    description: Mapped[str | None] = mapped_column(String(128))

    type_id: Mapped[int] = mapped_column(ForeignKey('transactions_types.id'))

    type: Mapped['TransactionType'] = relationship(back_populates='categories')

    def __repr__(self):
        return f'Category [#{self.id}]: {self.name}'


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(16, 2), default=Decimal('0.00'))
    datetime_created: Mapped[datetime] = mapped_column(default=func.now())
    datetime_updated: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    type_id: Mapped[int] = mapped_column(ForeignKey('transactions_types.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('transactions_categories.id'))

    account: Mapped['Account'] = relationship(backref='transactions')
    type: Mapped['TransactionType'] = relationship()
    category: Mapped['TransactionCategory'] = relationship()

    def __repr__(self):
        return f'Transaction [#{self.id}]: {self.amount} ({self.datetime_updated})'

    # TODO ???
    @property
    def user_uuid(self):
        return self.account.user_uuid
