# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .ledger_entry_extension_v1_ext import LedgerEntryExtensionV1Ext
from .sponsorship_descriptor import SponsorshipDescriptor

__all__ = ["LedgerEntryExtensionV1"]


class LedgerEntryExtensionV1:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerEntryExtensionV1
    {
        SponsorshipDescriptor sponsoringID;

        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        sponsoring_id: SponsorshipDescriptor,
        ext: LedgerEntryExtensionV1Ext,
    ) -> None:
        self.sponsoring_id = sponsoring_id
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.sponsoring_id.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntryExtensionV1":
        sponsoring_id = SponsorshipDescriptor.unpack(unpacker)
        ext = LedgerEntryExtensionV1Ext.unpack(unpacker)
        return cls(
            sponsoring_id=sponsoring_id,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerEntryExtensionV1":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntryExtensionV1":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sponsoring_id == other.sponsoring_id and self.ext == other.ext

    def __str__(self):
        out = [
            f"sponsoring_id={self.sponsoring_id}",
            f"ext={self.ext}",
        ]
        return f"<LedgerEntryExtensionV1 {[', '.join(out)]}>"
