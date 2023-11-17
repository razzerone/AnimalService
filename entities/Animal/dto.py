from entities.Animal.model import Animal
from entities.dto import DTO


class AnimalDTO(DTO):
    name: str
    order_id: int
