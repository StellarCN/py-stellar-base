# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_CHANGE_TRUST_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "no_issuer",
    -3: "invalid_limit",
    -4: "low_reserve",
    -5: "self_not_allowed",
    -6: "trust_line_missing",
    -7: "cannot_delete",
    -8: "not_auth_maintain_liabilities",
}
_CHANGE_TRUST_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "no_issuer": -2,
    "invalid_limit": -3,
    "low_reserve": -4,
    "self_not_allowed": -5,
    "trust_line_missing": -6,
    "cannot_delete": -7,
    "not_auth_maintain_liabilities": -8,
}
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ChangeTrustResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ChangeTrustResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _CHANGE_TRUST_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ChangeTrustResultCode:
        return cls(_CHANGE_TRUST_RESULT_CODE_REVERSE_MAP[json_value])
