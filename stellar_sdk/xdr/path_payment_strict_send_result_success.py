# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .claim_offer_atom import ClaimOfferAtom
from .simple_payment_result import SimplePaymentResult

__all__ = ["PathPaymentStrictSendResultSuccess"]


class PathPaymentStrictSendResultSuccess:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            ClaimOfferAtom offers<>;
            SimplePaymentResult last;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        offers: List[ClaimOfferAtom],
        last: SimplePaymentResult,
    ) -> None:
        if offers and len(offers) > 4294967295:
            raise ValueError(
                f"The maximum length of `offers` should be 4294967295, but got {len(offers)}."
            )
        self.offers = offers
        self.last = last

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.offers))
        for offer in self.offers:
            offer.pack(packer)
        self.last.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictSendResultSuccess":
        length = unpacker.unpack_uint()
        offers = []
        for _ in range(length):
            offers.append(ClaimOfferAtom.unpack(unpacker))
        last = SimplePaymentResult.unpack(unpacker)
        return cls(
            offers=offers,
            last=last,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "PathPaymentStrictSendResultSuccess":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictSendResultSuccess":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.offers == other.offers and self.last == other.last

    def __str__(self):
        out = [
            f"offers={self.offers}",
            f"last={self.last}",
        ]
        return f"<PathPaymentStrictSendResultSuccess {[', '.join(out)]}>"
