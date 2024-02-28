from pydantic import HttpUrl

from entities.model import Model


class Image(Model):
    id: int
    url: HttpUrl
