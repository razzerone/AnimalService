from pydantic import Field

from entities.dto import DTO


class AnimalDTO(DTO):
    name: str = Field(max_length=50)
    family_id: int
    description: str = Field(max_length=512)
    environment_description: str = Field(max_length=512)
    zoo_description: str = Field(max_length=512)
