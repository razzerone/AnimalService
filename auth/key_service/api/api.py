import datetime

from aiohttp import ClientSession

from auth.base_key_service import KeyService
from auth.key_service.api.exeptions import ServerUnavailable
from auth.key_service.api.key_model import Key


class APIKeyService(KeyService):
    def __init__(self, url: str):
        self._url = url
        self._key: Key | None = None

    @staticmethod
    async def _get_key_from_url(url: str) -> Key:
        async with ClientSession() as session:
            async with session.get(f'{url}/key') as resp:
                if resp.status != 200:
                    raise ServerUnavailable()
                json = await resp.read()
                return Key.model_validate_json(json)

    @property
    async def key(self) -> bytes:
        if self._key is None or self._key.expires_at > datetime.datetime.now(datetime.timezone.utc):
            self._key = await self._get_key_from_url(self._url)
        return bytes(self._key.key, 'ascii')
