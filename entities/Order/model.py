from pydantic import Field

from entities.Class.model import Class
from entities.model import Model


class Order(Model):
    id: int
    name: Field(str, max_length=50)
    class_: Class
