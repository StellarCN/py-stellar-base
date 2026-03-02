# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_CLAWBACK_CLAIMABLE_BALANCE_RESULT_CODE_MAP = {
    0: "success",
    -1: "does_not_exist",
    -2: "not_issuer",
    -3: "not_clawback_enabled",
}
_CLAWBACK_CLAIMABLE_BALANCE_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "does_not_exist": -1,
    "not_issuer": -2,
    "not_clawback_enabled": -3,
}
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ClawbackClaimableBalanceResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClawbackClaimableBalanceResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _CLAWBACK_CLAIMABLE_BALANCE_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ClawbackClaimableBalanceResultCode:
        return cls(_CLAWBACK_CLAIMABLE_BALANCE_RESULT_CODE_REVERSE_MAP[json_value])
