# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["ClawbackClaimableBalanceResultCode"]


class ClawbackClaimableBalanceResultCode(IntEnum):
    """
    XDR Source Code::

        enum ClawbackClaimableBalanceResultCode
        {
            // codes considered as "success" for the operation
            CLAWBACK_CLAIMABLE_BALANCE_SUCCESS = 0,

            // codes considered as "failure" for the operation
            CLAWBACK_CLAIMABLE_BALANCE_DOES_NOT_EXIST = -1,
            CLAWBACK_CLAIMABLE_BALANCE_NOT_ISSUER = -2,
            CLAWBACK_CLAIMABLE_BALANCE_NOT_CLAWBACK_ENABLED = -3
        };
    """

    CLAWBACK_CLAIMABLE_BALANCE_SUCCESS = 0
    CLAWBACK_CLAIMABLE_BALANCE_DOES_NOT_EXIST = -1
    CLAWBACK_CLAIMABLE_BALANCE_NOT_ISSUER = -2
    CLAWBACK_CLAIMABLE_BALANCE_NOT_CLAWBACK_ENABLED = -3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ClawbackClaimableBalanceResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClawbackClaimableBalanceResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ClawbackClaimableBalanceResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
