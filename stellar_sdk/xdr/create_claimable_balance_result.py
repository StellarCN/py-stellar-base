# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .claimable_balance_id import ClaimableBalanceID
from .create_claimable_balance_result_code import CreateClaimableBalanceResultCode

__all__ = ["CreateClaimableBalanceResult"]


class CreateClaimableBalanceResult:
    """
    XDR Source Code::

        union CreateClaimableBalanceResult switch (
            CreateClaimableBalanceResultCode code)
        {
        case CREATE_CLAIMABLE_BALANCE_SUCCESS:
            ClaimableBalanceID balanceID;
        case CREATE_CLAIMABLE_BALANCE_MALFORMED:
        case CREATE_CLAIMABLE_BALANCE_LOW_RESERVE:
        case CREATE_CLAIMABLE_BALANCE_NO_TRUST:
        case CREATE_CLAIMABLE_BALANCE_NOT_AUTHORIZED:
        case CREATE_CLAIMABLE_BALANCE_UNDERFUNDED:
            void;
        };
    """

    def __init__(
        self,
        code: CreateClaimableBalanceResultCode,
        balance_id: ClaimableBalanceID = None,
    ) -> None:
        self.code = code
        self.balance_id = balance_id

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_SUCCESS
        ):
            if self.balance_id is None:
                raise ValueError("balance_id should not be None.")
            self.balance_id.pack(packer)
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_MALFORMED
        ):
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_LOW_RESERVE
        ):
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NO_TRUST
        ):
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return
        if (
            self.code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_UNDERFUNDED
        ):
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> CreateClaimableBalanceResult:
        code = CreateClaimableBalanceResultCode.unpack(unpacker)
        if code == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_SUCCESS:
            balance_id = ClaimableBalanceID.unpack(unpacker)
            return cls(code=code, balance_id=balance_id)
        if code == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_MALFORMED:
            return cls(code=code)
        if (
            code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_LOW_RESERVE
        ):
            return cls(code=code)
        if code == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NO_TRUST:
            return cls(code=code)
        if (
            code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_NOT_AUTHORIZED
        ):
            return cls(code=code)
        if (
            code
            == CreateClaimableBalanceResultCode.CREATE_CLAIMABLE_BALANCE_UNDERFUNDED
        ):
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> CreateClaimableBalanceResult:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> CreateClaimableBalanceResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.code,
                self.balance_id,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.balance_id == other.balance_id

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(
            f"balance_id={self.balance_id}"
        ) if self.balance_id is not None else None
        return f"<CreateClaimableBalanceResult [{', '.join(out)}]>"
