from pydantic import Field

from entities.dto import DTO


class FamilyDTO(DTO):
    name: str = Field(max_length=100)
    order_id: int
