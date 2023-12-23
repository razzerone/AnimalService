from pydantic import Field

from entities.model import Model


class Class(Model):
    id: int
    name: Field(str, max_length=50)
