from pydantic import HttpUrl

from entities.dto import DTO


class ImageDTO(DTO):
    animal_id: int
    url: HttpUrl
