# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import String

__all__ = ["SCMetaV0"]


class SCMetaV0:
    """
    XDR Source Code::

        struct SCMetaV0
        {
            string key<>;
            string val<>;
        };
    """

    def __init__(
        self,
        key: bytes,
        val: bytes,
    ) -> None:
        self.key = key
        self.val = val

    def pack(self, packer: Packer) -> None:
        String(self.key, 4294967295).pack(packer)
        String(self.val, 4294967295).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCMetaV0:
        key = String.unpack(unpacker)
        val = String.unpack(unpacker)
        return cls(
            key=key,
            val=val,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCMetaV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCMetaV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.key,
                self.val,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key and self.val == other.val

    def __repr__(self):
        out = [
            f"key={self.key}",
            f"val={self.val}",
        ]
        return f"<SCMetaV0 [{', '.join(out)}]>"
