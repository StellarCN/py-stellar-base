# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_SET_OPTIONS_RESULT_CODE_MAP = {
    0: "success",
    -1: "low_reserve",
    -2: "too_many_signers",
    -3: "bad_flags",
    -4: "invalid_inflation",
    -5: "cant_change",
    -6: "unknown_flag",
    -7: "threshold_out_of_range",
    -8: "bad_signer",
    -9: "invalid_home_domain",
    -10: "auth_revocable_required",
}
_SET_OPTIONS_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "low_reserve": -1,
    "too_many_signers": -2,
    "bad_flags": -3,
    "invalid_inflation": -4,
    "cant_change": -5,
    "unknown_flag": -6,
    "threshold_out_of_range": -7,
    "bad_signer": -8,
    "invalid_home_domain": -9,
    "auth_revocable_required": -10,
}
__all__ = ["SetOptionsResultCode"]


class SetOptionsResultCode(IntEnum):
    """
    XDR Source Code::

        enum SetOptionsResultCode
        {
            // codes considered as "success" for the operation
            SET_OPTIONS_SUCCESS = 0,
            // codes considered as "failure" for the operation
            SET_OPTIONS_LOW_RESERVE = -1,      // not enough funds to add a signer
            SET_OPTIONS_TOO_MANY_SIGNERS = -2, // max number of signers already reached
            SET_OPTIONS_BAD_FLAGS = -3,        // invalid combination of clear/set flags
            SET_OPTIONS_INVALID_INFLATION = -4,      // inflation account does not exist
            SET_OPTIONS_CANT_CHANGE = -5,            // can no longer change this option
            SET_OPTIONS_UNKNOWN_FLAG = -6,           // can't set an unknown flag
            SET_OPTIONS_THRESHOLD_OUT_OF_RANGE = -7, // bad value for weight/threshold
            SET_OPTIONS_BAD_SIGNER = -8,             // signer cannot be masterkey
            SET_OPTIONS_INVALID_HOME_DOMAIN = -9,    // malformed home domain
            SET_OPTIONS_AUTH_REVOCABLE_REQUIRED =
                -10 // auth revocable is required for clawback
        };
    """

    SET_OPTIONS_SUCCESS = 0
    SET_OPTIONS_LOW_RESERVE = -1
    SET_OPTIONS_TOO_MANY_SIGNERS = -2
    SET_OPTIONS_BAD_FLAGS = -3
    SET_OPTIONS_INVALID_INFLATION = -4
    SET_OPTIONS_CANT_CHANGE = -5
    SET_OPTIONS_UNKNOWN_FLAG = -6
    SET_OPTIONS_THRESHOLD_OUT_OF_RANGE = -7
    SET_OPTIONS_BAD_SIGNER = -8
    SET_OPTIONS_INVALID_HOME_DOMAIN = -9
    SET_OPTIONS_AUTH_REVOCABLE_REQUIRED = -10

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SetOptionsResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SetOptionsResultCode:
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
    def from_xdr(cls, xdr: str) -> SetOptionsResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SetOptionsResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _SET_OPTIONS_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> SetOptionsResultCode:
        return cls(_SET_OPTIONS_RESULT_CODE_REVERSE_MAP[json_value])
