import os
from pathlib import Path

from auth.base_key_service import KeyService


class LocalKeyService(KeyService):
    def __init__(self, path: os.PathLike = None):
        if path is None:
            path = Path('./rs256/rs256_jwt.pub')

        with open(path, 'rb') as f:
            self._key = f.read()

    @property
    async def key(self) -> bytes:
        return self._key
