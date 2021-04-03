# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .claimable_balance_entry_extension_v1_ext import (
    ClaimableBalanceEntryExtensionV1Ext,
)
from .uint32 import Uint32

__all__ = ["ClaimableBalanceEntryExtensionV1"]


class ClaimableBalanceEntryExtensionV1:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ClaimableBalanceEntryExtensionV1
    {
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;

        uint32 flags; // see ClaimableBalanceFlags
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ext: ClaimableBalanceEntryExtensionV1Ext,
        flags: Uint32,
    ) -> None:
        self.ext = ext
        self.flags = flags

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.flags.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClaimableBalanceEntryExtensionV1":
        ext = ClaimableBalanceEntryExtensionV1Ext.unpack(unpacker)
        flags = Uint32.unpack(unpacker)
        return cls(
            ext=ext,
            flags=flags,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ClaimableBalanceEntryExtensionV1":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClaimableBalanceEntryExtensionV1":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ext == other.ext and self.flags == other.flags

    def __str__(self):
        out = [
            f"ext={self.ext}",
            f"flags={self.flags}",
        ]
        return f"<ClaimableBalanceEntryExtensionV1 {[', '.join(out)]}>"
