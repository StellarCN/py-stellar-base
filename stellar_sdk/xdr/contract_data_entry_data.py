# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_val import SCVal
from .uint32 import Uint32

__all__ = ["ContractDataEntryData"]


class ContractDataEntryData:
    """
    XDR Source Code::

        struct
            {
                uint32 flags;
                SCVal val;
            }
    """

    def __init__(
        self,
        flags: Uint32,
        val: SCVal,
    ) -> None:
        self.flags = flags
        self.val = val

    def pack(self, packer: Packer) -> None:
        self.flags.pack(packer)
        self.val.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractDataEntryData:
        flags = Uint32.unpack(unpacker)
        val = SCVal.unpack(unpacker)
        return cls(
            flags=flags,
            val=val,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractDataEntryData:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractDataEntryData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.flags,
                self.val,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.flags == other.flags and self.val == other.val

    def __str__(self):
        out = [
            f"flags={self.flags}",
            f"val={self.val}",
        ]
        return f"<ContractDataEntryData [{', '.join(out)}]>"
