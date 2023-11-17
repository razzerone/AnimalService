from entities.Order.model import Order
from entities.model import Model


class Animal(Model):
    id: int
    name: str
    order: Order
