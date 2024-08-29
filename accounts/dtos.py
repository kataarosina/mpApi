from pydantic import BaseModel

from currencies.dtos import CurrencyDTO


class AccountCreateDTO(BaseModel):
    name: str
    description: str
    currency_id: int


class AccountDTO(AccountCreateDTO):
    id: int


class AccountDTOWithRel(AccountDTO):
    currency: CurrencyDTO

# # Если мне когда-то понадобится что-то отсюда испортировать в accounts/dtos.py, это вызовет циклически импорт.
# # Решением будет то, что снизу.
# class AccountDTOWithRel(AccountDTO):
#     currency: 'CurrencyDTO'
#
#     class Config:
#         # Это нужно для того, что бы pydantic понял, что я использую имя класса для currency
#         # вместо прямого указания класса.
#         allow_population_by_field_name = True
#
#
# # Вызываю потому что выше использовал неявное указание типа для поля currency и allow_population_by_field_name = True
# AccountDTOWithRel.model_rebuild()
