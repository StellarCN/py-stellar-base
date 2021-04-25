# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *
from .scp_history_entry_v0 import SCPHistoryEntryV0
from ..exceptions import ValueError

__all__ = ["SCPHistoryEntry"]


class SCPHistoryEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union SCPHistoryEntry switch (int v)
    {
    case 0:
        SCPHistoryEntryV0 v0;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        v: int,
        v0: SCPHistoryEntryV0 = None,
    ) -> None:
        self.v = v
        self.v0 = v0

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPHistoryEntry":
        v = Integer.unpack(unpacker)
        if v == 0:
            v0 = SCPHistoryEntryV0.unpack(unpacker)
            if v0 is None:
                raise ValueError("v0 should not be None.")
            return cls(v, v0=v0)
        return cls(v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCPHistoryEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPHistoryEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v0 == other.v0

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        return f"<SCPHistoryEntry {[', '.join(out)]}>"
