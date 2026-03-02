# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_EXTEND_FOOTPRINT_TTL_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "resource_limit_exceeded",
    -3: "insufficient_refundable_fee",
}
_EXTEND_FOOTPRINT_TTL_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "resource_limit_exceeded": -2,
    "insufficient_refundable_fee": -3,
}
__all__ = ["ExtendFootprintTTLResultCode"]


class ExtendFootprintTTLResultCode(IntEnum):
    """
    XDR Source Code::

        enum ExtendFootprintTTLResultCode
        {
            // codes considered as "success" for the operation
            EXTEND_FOOTPRINT_TTL_SUCCESS = 0,

            // codes considered as "failure" for the operation
            EXTEND_FOOTPRINT_TTL_MALFORMED = -1,
            EXTEND_FOOTPRINT_TTL_RESOURCE_LIMIT_EXCEEDED = -2,
            EXTEND_FOOTPRINT_TTL_INSUFFICIENT_REFUNDABLE_FEE = -3
        };
    """

    EXTEND_FOOTPRINT_TTL_SUCCESS = 0
    EXTEND_FOOTPRINT_TTL_MALFORMED = -1
    EXTEND_FOOTPRINT_TTL_RESOURCE_LIMIT_EXCEEDED = -2
    EXTEND_FOOTPRINT_TTL_INSUFFICIENT_REFUNDABLE_FEE = -3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ExtendFootprintTTLResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ExtendFootprintTTLResultCode:
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
    def from_xdr(cls, xdr: str) -> ExtendFootprintTTLResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ExtendFootprintTTLResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _EXTEND_FOOTPRINT_TTL_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ExtendFootprintTTLResultCode:
        return cls(_EXTEND_FOOTPRINT_TTL_RESULT_CODE_REVERSE_MAP[json_value])
