from abc import ABC

from pydantic import BaseModel


class Model(ABC, BaseModel):
    ...
