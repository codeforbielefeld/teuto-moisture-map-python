import os


def get_secret(name: str) -> str | None:
    secret_file = os.environ.get(f"{name}_FILE")
    return open(secret_file, "r").read().strip() if secret_file else os.environ.get(name)


def get_secret_or_fail(name: str) -> str:
    secret_file = os.environ.get(f"{name}_FILE")
    return open(secret_file, "r").read().strip() if secret_file else os.environ[name]
