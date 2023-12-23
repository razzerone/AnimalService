from pydantic import Field

from entities.Animal.model import Animal
from entities.dto import DTO


class AnimalDTO(DTO):
    name: str = Field(max_length=50)
    order_id: int
