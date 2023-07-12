# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["ChangeTrustResultCode"]


class ChangeTrustResultCode(IntEnum):
    """
    XDR Source Code::

        enum ChangeTrustResultCode
        {
            // codes considered as "success" for the operation
            CHANGE_TRUST_SUCCESS = 0,
            // codes considered as "failure" for the operation
            CHANGE_TRUST_MALFORMED = -1,     // bad input
            CHANGE_TRUST_NO_ISSUER = -2,     // could not find issuer
            CHANGE_TRUST_INVALID_LIMIT = -3, // cannot drop limit below balance
                                             // cannot create with a limit of 0
            CHANGE_TRUST_LOW_RESERVE =
                -4, // not enough funds to create a new trust line,
            CHANGE_TRUST_SELF_NOT_ALLOWED = -5,   // trusting self is not allowed
            CHANGE_TRUST_TRUST_LINE_MISSING = -6, // Asset trustline is missing for pool
            CHANGE_TRUST_CANNOT_DELETE =
                -7, // Asset trustline is still referenced in a pool
            CHANGE_TRUST_NOT_AUTH_MAINTAIN_LIABILITIES =
                -8 // Asset trustline is deauthorized
        };
    """

    CHANGE_TRUST_SUCCESS = 0
    CHANGE_TRUST_MALFORMED = -1
    CHANGE_TRUST_NO_ISSUER = -2
    CHANGE_TRUST_INVALID_LIMIT = -3
    CHANGE_TRUST_LOW_RESERVE = -4
    CHANGE_TRUST_SELF_NOT_ALLOWED = -5
    CHANGE_TRUST_TRUST_LINE_MISSING = -6
    CHANGE_TRUST_CANNOT_DELETE = -7
    CHANGE_TRUST_NOT_AUTH_MAINTAIN_LIABILITIES = -8

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ChangeTrustResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ChangeTrustResultCode:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ChangeTrustResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
