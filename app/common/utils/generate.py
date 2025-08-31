from uuid import uuid4
from os import urandom

__all__ = ["generate_uuid", "generate_key"]


def generate_uuid() -> str:
    return str(uuid4())


def generate_key(length: int = 32) -> str:
    return urandom(length).hex()
