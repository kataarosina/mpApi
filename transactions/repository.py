from core.database.repository import SQLAlchemyModelRepository

from transactions.models import TransactionType, TransactionCategory, Transaction


class TransactionTypeRepository(SQLAlchemyModelRepository):

    model_class = TransactionType


class TransactionCategoryRepository(SQLAlchemyModelRepository):

    model_class = TransactionCategory


class TransactionRepository(SQLAlchemyModelRepository):

    model_class = Transaction


# TODO so... will i use it?
