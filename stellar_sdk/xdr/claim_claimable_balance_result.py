# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .claim_claimable_balance_result_code import ClaimClaimableBalanceResultCode

__all__ = ["ClaimClaimableBalanceResult"]


class ClaimClaimableBalanceResult:
    """
    XDR Source Code::

        union ClaimClaimableBalanceResult switch (ClaimClaimableBalanceResultCode code)
        {
        case CLAIM_CLAIMABLE_BALANCE_SUCCESS:
            void;
        case CLAIM_CLAIMABLE_BALANCE_DOES_NOT_EXIST:
        case CLAIM_CLAIMABLE_BALANCE_CANNOT_CLAIM:
        case CLAIM_CLAIMABLE_BALANCE_LINE_FULL:
        case CLAIM_CLAIMABLE_BALANCE_NO_TRUST:
        case CLAIM_CLAIMABLE_BALANCE_NOT_AUTHORIZED:
            void;
        };
    """

    def __init__(
        self,
        code: ClaimClaimableBalanceResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_SUCCESS:
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_DOES_NOT_EXIST
        ):
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_CANNOT_CLAIM
        ):
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_LINE_FULL
        ):
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NO_TRUST
        ):
            return
        if (
            self.code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ClaimClaimableBalanceResult:
        code = ClaimClaimableBalanceResultCode.unpack(unpacker)
        if code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_SUCCESS:
            return cls(code=code)
        if (
            code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_DOES_NOT_EXIST
        ):
            return cls(code=code)
        if code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_CANNOT_CLAIM:
            return cls(code=code)
        if code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_LINE_FULL:
            return cls(code=code)
        if code == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NO_TRUST:
            return cls(code=code)
        if (
            code
            == ClaimClaimableBalanceResultCode.CLAIM_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimClaimableBalanceResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ClaimClaimableBalanceResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash((self.code,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<ClaimClaimableBalanceResult [{', '.join(out)}]>"
