from pydantic import Field

from entities.Order.model import Order
from entities.dto import DTO


class OrderDTO(DTO):
    name: Field(str, max_length=50)
    class_id: int
