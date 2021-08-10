# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .liabilities import Liabilities
from .trust_line_entry_v1_ext import TrustLineEntryV1Ext

__all__ = ["TrustLineEntryV1"]


class TrustLineEntryV1:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
            {
                Liabilities liabilities;

                union switch (int v)
                {
                case 0:
                    void;
                }
                ext;
            }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        liabilities: Liabilities,
        ext: TrustLineEntryV1Ext,
    ) -> None:
        self.liabilities = liabilities
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.liabilities.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TrustLineEntryV1":
        liabilities = Liabilities.unpack(unpacker)
        ext = TrustLineEntryV1Ext.unpack(unpacker)
        return cls(
            liabilities=liabilities,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TrustLineEntryV1":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TrustLineEntryV1":
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
        return f"<TrustLineEntryV1 {[', '.join(out)]}>"
