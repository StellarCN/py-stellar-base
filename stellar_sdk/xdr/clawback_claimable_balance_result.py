# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .clawback_claimable_balance_result_code import ClawbackClaimableBalanceResultCode

__all__ = ["ClawbackClaimableBalanceResult"]


class ClawbackClaimableBalanceResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union ClawbackClaimableBalanceResult switch (ClawbackClaimableBalanceResultCode code)
    {
    case CLAWBACK_CLAIMABLE_BALANCE_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: ClawbackClaimableBalanceResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_SUCCESS
        ):
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClawbackClaimableBalanceResult":
        code = ClawbackClaimableBalanceResultCode.unpack(unpacker)
        if (
            code
            == ClawbackClaimableBalanceResultCode.CLAWBACK_CLAIMABLE_BALANCE_SUCCESS
        ):
            return cls(code)
        return cls(code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ClawbackClaimableBalanceResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClawbackClaimableBalanceResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<ClawbackClaimableBalanceResult {[', '.join(out)]}>"
