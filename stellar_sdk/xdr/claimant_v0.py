# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .claim_predicate import ClaimPredicate

__all__ = ["ClaimantV0"]


class ClaimantV0:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AccountID destination;    // The account that can use this condition
            ClaimPredicate predicate; // Claimable if predicate is true
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        destination: AccountID,
        predicate: ClaimPredicate,
    ) -> None:
        self.destination = destination
        self.predicate = predicate

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.predicate.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClaimantV0":
        destination = AccountID.unpack(unpacker)
        predicate = ClaimPredicate.unpack(unpacker)
        return cls(
            destination=destination,
            predicate=predicate,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ClaimantV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClaimantV0":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.destination == other.destination and self.predicate == other.predicate
        )

    def __str__(self):
        out = [
            f"destination={self.destination}",
            f"predicate={self.predicate}",
        ]
        return f"<ClaimantV0 {[', '.join(out)]}>"
