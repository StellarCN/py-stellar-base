# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64

__all__ = ["SCNonceKey"]


class SCNonceKey:
    """
    XDR Source Code::

        struct SCNonceKey {
            int64 nonce;
        };
    """

    def __init__(
        self,
        nonce: Int64,
    ) -> None:
        self.nonce = nonce

    def pack(self, packer: Packer) -> None:
        self.nonce.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCNonceKey:
        nonce = Int64.unpack(unpacker)
        return cls(
            nonce=nonce,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCNonceKey:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCNonceKey:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.nonce,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.nonce == other.nonce

    def __repr__(self):
        out = [
            f"nonce={self.nonce}",
        ]
        return f"<SCNonceKey [{', '.join(out)}]>"
