from pydantic import BaseModel


class CurrencyCreateDTO(BaseModel):
    name: str
    symbol: str
    code: str


class CurrencyDTO(CurrencyCreateDTO):
    id: int
