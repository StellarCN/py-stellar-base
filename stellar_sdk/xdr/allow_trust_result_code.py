# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_ALLOW_TRUST_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "no_trust_line",
    -3: "trust_not_required",
    -4: "cant_revoke",
    -5: "self_not_allowed",
    -6: "low_reserve",
}
_ALLOW_TRUST_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "no_trust_line": -2,
    "trust_not_required": -3,
    "cant_revoke": -4,
    "self_not_allowed": -5,
    "low_reserve": -6,
}
__all__ = ["AllowTrustResultCode"]


class AllowTrustResultCode(IntEnum):
    """
    XDR Source Code::

        enum AllowTrustResultCode
        {
            // codes considered as "success" for the operation
            ALLOW_TRUST_SUCCESS = 0,
            // codes considered as "failure" for the operation
            ALLOW_TRUST_MALFORMED = -1,     // asset is not ASSET_TYPE_ALPHANUM
            ALLOW_TRUST_NO_TRUST_LINE = -2, // trustor does not have a trustline
                                            // source account does not require trust
            ALLOW_TRUST_TRUST_NOT_REQUIRED = -3,
            ALLOW_TRUST_CANT_REVOKE = -4,      // source account can't revoke trust,
            ALLOW_TRUST_SELF_NOT_ALLOWED = -5, // trusting self is not allowed
            ALLOW_TRUST_LOW_RESERVE = -6       // claimable balances can't be created
                                               // on revoke due to low reserves
        };
    """

    ALLOW_TRUST_SUCCESS = 0
    ALLOW_TRUST_MALFORMED = -1
    ALLOW_TRUST_NO_TRUST_LINE = -2
    ALLOW_TRUST_TRUST_NOT_REQUIRED = -3
    ALLOW_TRUST_CANT_REVOKE = -4
    ALLOW_TRUST_SELF_NOT_ALLOWED = -5
    ALLOW_TRUST_LOW_RESERVE = -6

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> AllowTrustResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AllowTrustResultCode:
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
    def from_xdr(cls, xdr: str) -> AllowTrustResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AllowTrustResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _ALLOW_TRUST_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> AllowTrustResultCode:
        return cls(_ALLOW_TRUST_RESULT_CODE_REVERSE_MAP[json_value])
