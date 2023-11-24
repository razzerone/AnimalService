import binascii

from jwt import JWT, jwk_from_pem
from jwt.exceptions import JWTException, JWTDecodeError

from auth.base_key_service import KeyService
from auth.key_service.exceptions import InvalidToken


class Auth:
    jwt = JWT()

    def __init__(self, _key_service: KeyService):
        self._key_service = _key_service

    async def decode(self, token: str):
        key = await self._key_service.key
        try:
            msg = self.jwt.decode(token, jwk_from_pem(key), do_time_check=True)
        except binascii.Error as e:
            raise InvalidToken()
        except JWTDecodeError as e:
            raise InvalidToken()
        return msg
