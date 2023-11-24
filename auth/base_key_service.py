from abc import ABC, abstractmethod


class KeyService(ABC):
    @property
    async def key(self) -> bytes:
        raise NotImplementedError
