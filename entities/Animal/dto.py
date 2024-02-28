from decimal import Decimal
from typing import Optional

from pydantic import Field, HttpUrl

from entities.dto import DTO


class AnimalDTO(DTO):
    name: str = Field(max_length=100)
    family_id: int
    description: Optional[str] = Field(max_length=1024)
    environment_description: Optional[str] = Field(max_length=1024)
    zoo_description: Optional[str] = Field(max_length=1024)
    geolocation: tuple[Decimal, Decimal]
    qr_url: HttpUrl
    map_icon_url: HttpUrl
    list_icon_url: HttpUrl
    audio_url: HttpUrl
