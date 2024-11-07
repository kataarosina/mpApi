from pydantic import BaseModel


class PersonCreateDTO(BaseModel):
    name: str
    surname: str
    role: str
    department_id: int


class PersonDTO(PersonCreateDTO):
    id: int

