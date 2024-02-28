from decimal import Decimal
from typing import Optional

from pydantic import Field, HttpUrl

from entities.Family.model import Family
from entities.Image.model import Image
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
    geolocation: tuple[Decimal, Decimal]
    qr_url: HttpUrl
    map_icon_url: HttpUrl
    list_icon_url: HttpUrl
    audio_url: HttpUrl
    images: list[Image]
