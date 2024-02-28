from pydantic import Field

from entities.model import Model


class Class(Model):
    id: int
    name: str = Field(max_length=100)
