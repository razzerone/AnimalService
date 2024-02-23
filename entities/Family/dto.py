from pydantic import Field

from entities.dto import DTO


class FamilyDTO(DTO):
    name: str = Field(max_length=50)
    order_id: int
