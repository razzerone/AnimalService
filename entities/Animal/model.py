from pydantic import Field

from entities.Family.model import Family
from entities.model import Model


class Animal(Model):
    id: int
    name: str = Field(max_length=50)
    family: Family
