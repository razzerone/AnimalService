from pydantic import Field

from entities.model import Model


class Parameter(Model):
    id: int
    key: str = Field(max_length=50)
    value: str = Field(max_length=50)
