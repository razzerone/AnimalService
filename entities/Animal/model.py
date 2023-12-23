from pydantic import Field

from entities.Order.model import Order
from entities.model import Model


class Animal(Model):
    id: int
    name: Field(str, max_length=50)
    order: Order
