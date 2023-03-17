import hmac
from hashlib import sha256

from tmm_api.common.secrets import get_secret_or_fail


__auth_secret = None


def get_auth_secret() -> bytes:
    global __auth_secret
    if __auth_secret is None:
        __auth_secret = str.encode(get_secret_or_fail("TMM_AUTH_SECRET"))
    return __auth_secret


def get_digest(user: str) -> str:
    return hmac.new(get_auth_secret(), str.encode(user), sha256).hexdigest()


def is_auth(user: str, digest: str):
    return hmac.compare_digest(digest, get_digest(user))
