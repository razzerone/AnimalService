from pydantic import Field

from entities.dto import DTO


class AnimalDTO(DTO):
    name: str = Field(max_length=50)
    family_id: int
