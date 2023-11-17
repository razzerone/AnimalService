from entities.Order.model import Order
from entities.dto import DTO


class OrderDTO(DTO):
    name: str
    class_id: int
