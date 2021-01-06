# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .int64 import Int64

__all__ = ["CreateAccountOp"]


class CreateAccountOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct CreateAccountOp
    {
        AccountID destination; // account to create
        int64 startingBalance; // amount they end up with
    };
    ----------------------------------------------------------------
    """

    def __init__(self, destination: AccountID, starting_balance: Int64,) -> None:
        self.destination = destination
        self.starting_balance = starting_balance

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.starting_balance.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "CreateAccountOp":
        destination = AccountID.unpack(unpacker)
        starting_balance = Int64.unpack(unpacker)
        return cls(destination=destination, starting_balance=starting_balance,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "CreateAccountOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "CreateAccountOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.destination == other.destination
            and self.starting_balance == other.starting_balance
        )

    def __str__(self):
        out = [
            f"destination={self.destination}",
            f"starting_balance={self.starting_balance}",
        ]
        return f"<CreateAccountOp {[', '.join(out)]}>"
