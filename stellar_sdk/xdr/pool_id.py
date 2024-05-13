# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hash import Hash

__all__ = ["PoolID"]


class PoolID:
    """
    XDR Source Code::

        typedef Hash PoolID;
    """

    def __init__(self, pool_id: Hash) -> None:
        self.pool_id = pool_id

    def pack(self, packer: Packer) -> None:
        self.pool_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> PoolID:
        pool_id = Hash.unpack(unpacker)
        return cls(pool_id)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PoolID:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> PoolID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.pool_id)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.pool_id == other.pool_id

    def __repr__(self):
        return f"<PoolID [pool_id={self.pool_id}]>"
