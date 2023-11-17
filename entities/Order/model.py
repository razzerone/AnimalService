from entities.Class.model import Class
from entities.model import Model


class Order(Model):
    id: int
    name: str
    class_: Class
