from pydantic import Field

from entities.dto import DTO


class ParameterDTO(DTO):
    animal_id: int
    key: str = Field(max_length=100)
    value: str = Field(max_length=100)
