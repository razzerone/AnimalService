import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from jwt import (
    JWT,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime

instance = JWT()

message = {
    'iss': 'https://example.com/',
    'sub': 'yosida95',
    'iat': get_int_from_datetime(datetime.now(timezone.utc)),
    'exp': get_int_from_datetime(
        datetime.now(timezone.utc) + timedelta(days=30)),
}


def get_token(msg: dict[str, Any], path: os.PathLike = '../rs256/rs256_jwt.pem') -> str:
    with open(path, 'rb') as f:
        signing_key = jwk_from_pem(f.read())

    return instance.encode(msg, signing_key, alg='RS256')


if __name__ == '__main__':
    t = get_token(message, path=Path('rs256_jwt.pem'))
    print(t)
    with open('token.jwt', 'w') as f:
        f.write(t)
