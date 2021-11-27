# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from ..type_checked import type_checked
from .base import Integer
from .trust_line_entry_extension_v2 import TrustLineEntryExtensionV2

__all__ = ["TrustLineEntryV1Ext"]


@type_checked
class TrustLineEntryV1Ext:
    """
    XDR Source Code::

        union switch (int v)
                    {
                    case 0:
                        void;
                    case 2:
                        TrustLineEntryExtensionV2 v2;
                    }
    """

    def __init__(
        self,
        v: int,
        v2: TrustLineEntryExtensionV2 = None,
    ) -> None:
        self.v = v
        self.v2 = v2

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 2:
            if self.v2 is None:
                raise ValueError("v2 should not be None.")
            self.v2.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TrustLineEntryV1Ext":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 2:
            v2 = TrustLineEntryExtensionV2.unpack(unpacker)
            return cls(v=v, v2=v2)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TrustLineEntryV1Ext":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TrustLineEntryV1Ext":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v2 == other.v2

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v2={self.v2}") if self.v2 is not None else None
        return f"<TrustLineEntryV1Ext {[', '.join(out)]}>"
