# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_RESTORE_FOOTPRINT_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "resource_limit_exceeded",
    -3: "insufficient_refundable_fee",
}
_RESTORE_FOOTPRINT_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "resource_limit_exceeded": -2,
    "insufficient_refundable_fee": -3,
}
__all__ = ["RestoreFootprintResultCode"]


class RestoreFootprintResultCode(IntEnum):
    """
    XDR Source Code::

        enum RestoreFootprintResultCode
        {
            // codes considered as "success" for the operation
            RESTORE_FOOTPRINT_SUCCESS = 0,

            // codes considered as "failure" for the operation
            RESTORE_FOOTPRINT_MALFORMED = -1,
            RESTORE_FOOTPRINT_RESOURCE_LIMIT_EXCEEDED = -2,
            RESTORE_FOOTPRINT_INSUFFICIENT_REFUNDABLE_FEE = -3
        };
    """

    RESTORE_FOOTPRINT_SUCCESS = 0
    RESTORE_FOOTPRINT_MALFORMED = -1
    RESTORE_FOOTPRINT_RESOURCE_LIMIT_EXCEEDED = -2
    RESTORE_FOOTPRINT_INSUFFICIENT_REFUNDABLE_FEE = -3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> RestoreFootprintResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> RestoreFootprintResultCode:
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
    def from_xdr(cls, xdr: str) -> RestoreFootprintResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> RestoreFootprintResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _RESTORE_FOOTPRINT_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> RestoreFootprintResultCode:
        return cls(_RESTORE_FOOTPRINT_RESULT_CODE_REVERSE_MAP[json_value])
