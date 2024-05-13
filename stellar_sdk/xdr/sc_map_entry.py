# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_val import SCVal

__all__ = ["SCMapEntry"]


class SCMapEntry:
    """
    XDR Source Code::

        struct SCMapEntry
        {
            SCVal key;
            SCVal val;
        };
    """

    def __init__(
        self,
        key: SCVal,
        val: SCVal,
    ) -> None:
        self.key = key
        self.val = val

    def pack(self, packer: Packer) -> None:
        self.key.pack(packer)
        self.val.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCMapEntry:
        key = SCVal.unpack(unpacker)
        val = SCVal.unpack(unpacker)
        return cls(
            key=key,
            val=val,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCMapEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCMapEntry:
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
        return f"<SCMapEntry [{', '.join(out)}]>"
