import hashlib


def hash256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()
