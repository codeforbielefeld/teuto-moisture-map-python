import os
from cachetools import cached

from tmm_api.common.aws_secrets import get_aws_secret


@cached(cache={})
def get_secret(name: str) -> str | None:
    if secret_file := os.environ.get(f"{name}_FILE"):
        return open(secret_file, "r").read().strip()
    elif secret_id := os.environ.get(f"{name}_ID"):
        return get_aws_secret(secret_id)
    else:
        return os.environ.get(name)


def get_secret_or_fail(name: str) -> str:
    secret = get_secret(name)
    assert (
        secret is not None
    ), f"Could not load secret {name}, set either of the env variables {name}, {name}_FILE or {name}_ID"
    return secret
