from decimal import Decimal
from typing import Optional

from pydantic import Field, HttpUrl

from entities.dto import DTO


class AnimalDTO(DTO):
    name: str = Field(max_length=50)
    family_id: int
    description: Optional[str] = Field(max_length=512)
    environment_description: Optional[str] = Field(max_length=512)
    zoo_description: Optional[str] = Field(max_length=512)
    geolocation: tuple[Decimal, Decimal]
    qr_url: HttpUrl
    map_icon_url: HttpUrl
    list_icon_url: HttpUrl
    audio_url: HttpUrl
