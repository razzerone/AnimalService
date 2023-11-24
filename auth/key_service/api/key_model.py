import datetime

from pydantic import BaseModel


class Key(BaseModel):
    id: int
    created_at: datetime.datetime
    expires_at: datetime.datetime
    key_algorithm: str
    key: str
