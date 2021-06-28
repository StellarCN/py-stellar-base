# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_entry_extension_v1_ext import AccountEntryExtensionV1Ext
from .liabilities import Liabilities

__all__ = ["AccountEntryExtensionV1"]


class AccountEntryExtensionV1:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct AccountEntryExtensionV1
    {
        Liabilities liabilities;

        union switch (int v)
        {
        case 0:
            void;
        case 2:
            AccountEntryExtensionV2 v2;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        liabilities: Liabilities,
        ext: AccountEntryExtensionV1Ext,
    ) -> None:
        self.liabilities = liabilities
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.liabilities.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountEntryExtensionV1":
        liabilities = Liabilities.unpack(unpacker)
        ext = AccountEntryExtensionV1Ext.unpack(unpacker)
        return cls(
            liabilities=liabilities,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AccountEntryExtensionV1":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountEntryExtensionV1":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.liabilities == other.liabilities and self.ext == other.ext

    def __str__(self):
        out = [
            f"liabilities={self.liabilities}",
            f"ext={self.ext}",
        ]
        return f"<AccountEntryExtensionV1 {[', '.join(out)]}>"
