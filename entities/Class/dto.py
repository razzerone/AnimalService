from pydantic import Field

from entities.Class.model import Class
from entities.dto import DTO


class ClassDTO(DTO):
    name: Field(str, max_length=50)
