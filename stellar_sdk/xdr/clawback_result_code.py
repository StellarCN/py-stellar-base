# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_CLAWBACK_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "not_clawback_enabled",
    -3: "no_trust",
    -4: "underfunded",
}
_CLAWBACK_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "not_clawback_enabled": -2,
    "no_trust": -3,
    "underfunded": -4,
}
__all__ = ["ClawbackResultCode"]


class ClawbackResultCode(IntEnum):
    """
    XDR Source Code::

        enum ClawbackResultCode
        {
            // codes considered as "success" for the operation
            CLAWBACK_SUCCESS = 0,

            // codes considered as "failure" for the operation
            CLAWBACK_MALFORMED = -1,
            CLAWBACK_NOT_CLAWBACK_ENABLED = -2,
            CLAWBACK_NO_TRUST = -3,
            CLAWBACK_UNDERFUNDED = -4
        };
    """

    CLAWBACK_SUCCESS = 0
    CLAWBACK_MALFORMED = -1
    CLAWBACK_NOT_CLAWBACK_ENABLED = -2
    CLAWBACK_NO_TRUST = -3
    CLAWBACK_UNDERFUNDED = -4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ClawbackResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClawbackResultCode:
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
    def from_xdr(cls, xdr: str) -> ClawbackResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClawbackResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _CLAWBACK_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ClawbackResultCode:
        return cls(_CLAWBACK_RESULT_CODE_REVERSE_MAP[json_value])
