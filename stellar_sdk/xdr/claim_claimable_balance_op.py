# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .claimable_balance_id import ClaimableBalanceID

__all__ = ["ClaimClaimableBalanceOp"]


class ClaimClaimableBalanceOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ClaimClaimableBalanceOp
    {
        ClaimableBalanceID balanceID;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        balance_id: ClaimableBalanceID,
    ) -> None:
        self.balance_id = balance_id

    def pack(self, packer: Packer) -> None:
        self.balance_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClaimClaimableBalanceOp":
        balance_id = ClaimableBalanceID.unpack(unpacker)
        return cls(
            balance_id=balance_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ClaimClaimableBalanceOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClaimClaimableBalanceOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.balance_id == other.balance_id

    def __str__(self):
        out = [
            f"balance_id={self.balance_id}",
        ]
        return f"<ClaimClaimableBalanceOp {[', '.join(out)]}>"
