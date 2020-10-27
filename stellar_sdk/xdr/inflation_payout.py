# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .int64 import Int64

__all__ = ["InflationPayout"]


class InflationPayout:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct InflationPayout // or use PaymentResultAtom to limit types?
    {
        AccountID destination;
        int64 amount;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, destination: AccountID, amount: Int64,) -> None:
        self.destination = destination
        self.amount = amount

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.amount.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InflationPayout":
        destination = AccountID.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        return cls(destination=destination, amount=amount,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "InflationPayout":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InflationPayout":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.destination == other.destination and self.amount == other.amount

    def __str__(self):
        out = [
            f"destination={self.destination}",
            f"amount={self.amount}",
        ]
        return f"<InflationPayout {[', '.join(out)]}>"
