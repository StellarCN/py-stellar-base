# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_CLAIM_CLAIMABLE_BALANCE_RESULT_CODE_MAP = {
    0: "success",
    -1: "does_not_exist",
    -2: "cannot_claim",
    -3: "line_full",
    -4: "no_trust",
    -5: "not_authorized",
    -6: "trustline_frozen",
}
_CLAIM_CLAIMABLE_BALANCE_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "does_not_exist": -1,
    "cannot_claim": -2,
    "line_full": -3,
    "no_trust": -4,
    "not_authorized": -5,
    "trustline_frozen": -6,
}
__all__ = ["ClaimClaimableBalanceResultCode"]


class ClaimClaimableBalanceResultCode(IntEnum):
    """
    XDR Source Code::

        enum ClaimClaimableBalanceResultCode
        {
            CLAIM_CLAIMABLE_BALANCE_SUCCESS = 0,
            CLAIM_CLAIMABLE_BALANCE_DOES_NOT_EXIST = -1,
            CLAIM_CLAIMABLE_BALANCE_CANNOT_CLAIM = -2,
            CLAIM_CLAIMABLE_BALANCE_LINE_FULL = -3,
            CLAIM_CLAIMABLE_BALANCE_NO_TRUST = -4,
            CLAIM_CLAIMABLE_BALANCE_NOT_AUTHORIZED = -5,
            CLAIM_CLAIMABLE_BALANCE_TRUSTLINE_FROZEN = -6
        };
    """

    CLAIM_CLAIMABLE_BALANCE_SUCCESS = 0
    CLAIM_CLAIMABLE_BALANCE_DOES_NOT_EXIST = -1
    CLAIM_CLAIMABLE_BALANCE_CANNOT_CLAIM = -2
    CLAIM_CLAIMABLE_BALANCE_LINE_FULL = -3
    CLAIM_CLAIMABLE_BALANCE_NO_TRUST = -4
    CLAIM_CLAIMABLE_BALANCE_NOT_AUTHORIZED = -5
    CLAIM_CLAIMABLE_BALANCE_TRUSTLINE_FROZEN = -6

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ClaimClaimableBalanceResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimClaimableBalanceResultCode:
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
    def from_xdr(cls, xdr: str) -> ClaimClaimableBalanceResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimClaimableBalanceResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _CLAIM_CLAIMABLE_BALANCE_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ClaimClaimableBalanceResultCode:
        return cls(_CLAIM_CLAIMABLE_BALANCE_RESULT_CODE_REVERSE_MAP[json_value])
