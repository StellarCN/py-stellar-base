# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .int64 import Int64

__all__ = ["LedgerKeyOffer"]


class LedgerKeyOffer:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AccountID sellerID;
            int64 offerID;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, seller_id: AccountID, offer_id: Int64,) -> None:
        self.seller_id = seller_id
        self.offer_id = offer_id

    def pack(self, packer: Packer) -> None:
        self.seller_id.pack(packer)
        self.offer_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKeyOffer":
        seller_id = AccountID.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
        return cls(seller_id=seller_id, offer_id=offer_id,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerKeyOffer":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKeyOffer":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.seller_id == other.seller_id and self.offer_id == other.offer_id

    def __str__(self):
        out = [
            f"seller_id={self.seller_id}",
            f"offer_id={self.offer_id}",
        ]
        return f"<LedgerKeyOffer {[', '.join(out)]}>"
