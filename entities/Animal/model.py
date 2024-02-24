from pydantic import Field

from entities.Family.model import Family
from entities.Parameter.model import Parameter
from entities.model import Model


class Animal(Model):
    id: int
    name: str = Field(max_length=50)
    family: Family
    parameters: list[Parameter]
    description: str = Field(max_length=512)
    environment_description: str = Field(max_length=512)
    zoo_description: str = Field(max_length=512)
