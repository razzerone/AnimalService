from pydantic import Field

from entities.dto import DTO


class OrderDTO(DTO):
    name: str = Field(max_length=50)
    class_id: int
