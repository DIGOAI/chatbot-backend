import time
from typing import TypedDict, cast

import jwt

from src.config import Config

Payload = TypedDict('Payload', {
    'sub': str,
    'type': str,
    'role': str,
    'exp': int,
    'iat': int
})


def signJWT(user_id: str, keyType: str, role: str, exp_time_sec: int = 3600):
    # exp and iat in seconds since epoch (UTC) - https://www.rfc-editor.org/rfc/rfc7519#section-2
    payload: Payload = {
        "sub": user_id,
        "type": keyType,
        "role": role,
        "exp": int(time.time()) + exp_time_sec,
        "iat": int(time.time())
    }
    token = jwt.encode(payload=dict(payload), key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)  # type: ignore

    return token, payload


def decodeJWT(token: str) -> Payload | None:
    try:
        decoded_token = cast(Payload, jwt.decode(token, Config.JWT_SECRET, algorithms=[  # type: ignore
                             Config.JWT_ALGORITHM], options={"require": ["exp", "iat", "sub"]}))
        print(decoded_token)
        return decoded_token
    except:
        return None
