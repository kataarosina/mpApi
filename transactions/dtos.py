from datetime import datetime
from decimal import Decimal

from core.dtos import Base


# Without relationships
class TransactionTypeCreateDTO(Base):
    name: str


class TransactionTypeDTO(TransactionTypeCreateDTO):
    id: int


class TransactionCategoryCreateDTO(Base):
    name: str
    description: str | None
    type_id: int


class TransactionCategoryDTO(TransactionCategoryCreateDTO):
    id: int


class TransactionCreateDTO(Base):
    amount: Decimal
    type_id: int
    category_id: int


class TransactionUpdateDTO(TransactionCreateDTO):
    pass


class TransactionDTO(TransactionCreateDTO):
    id: int
    datetime_created: datetime
    datetime_updated: datetime


# With relationships
# Находится здесь, что бы использовать list[TransactionCategoryDTO] вместо list['TransactionCategoryDTO']
# Иначе ошибка: pydantic.errors.PydanticUndefinedAnnotation: name 'TransactionCategoryDTO' is not defined
class TransactionTypeRelDTO(TransactionTypeDTO):
    categories: list[TransactionCategoryDTO]


class TransactionCategoryRelDTO(TransactionCategoryDTO):
    type: TransactionTypeDTO


class TransactionRelDTO(TransactionDTO):
    type: TransactionTypeDTO
    category: TransactionCategoryDTO
