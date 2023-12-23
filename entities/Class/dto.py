from pydantic import Field

from entities.Class.model import Class
from entities.dto import DTO


class ClassDTO(DTO):
    name: str = Field(max_length=50)
