# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque

__all__ = ["EncryptedBody"]


class EncryptedBody:
    """
    XDR Source Code::

        typedef opaque EncryptedBody<64000>;
    """

    def __init__(self, encrypted_body: bytes) -> None:
        self.encrypted_body = encrypted_body

    def pack(self, packer: Packer) -> None:
        Opaque(self.encrypted_body, 64000, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> EncryptedBody:
        encrypted_body = Opaque.unpack(unpacker, 64000, False)
        return cls(encrypted_body)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> EncryptedBody:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> EncryptedBody:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.encrypted_body)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.encrypted_body == other.encrypted_body

    def __repr__(self):
        return f"<EncryptedBody [encrypted_body={self.encrypted_body}]>"
