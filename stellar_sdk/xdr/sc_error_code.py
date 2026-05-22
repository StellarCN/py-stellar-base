# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_SC_ERROR_CODE_MAP = {
    0: "arith_domain",
    1: "index_bounds",
    2: "invalid_input",
    3: "missing_value",
    4: "existing_value",
    5: "exceeded_limit",
    6: "invalid_action",
    7: "internal_error",
    8: "unexpected_type",
    9: "unexpected_size",
}
_SC_ERROR_CODE_REVERSE_MAP = {
    "arith_domain": 0,
    "index_bounds": 1,
    "invalid_input": 2,
    "missing_value": 3,
    "existing_value": 4,
    "exceeded_limit": 5,
    "invalid_action": 6,
    "internal_error": 7,
    "unexpected_type": 8,
    "unexpected_size": 9,
}
__all__ = ["SCErrorCode"]


class SCErrorCode(IntEnum):
    """
    XDR Source Code::

        enum SCErrorCode
        {
            SCEC_ARITH_DOMAIN = 0,      // Some arithmetic was undefined (overflow, divide-by-zero).
            SCEC_INDEX_BOUNDS = 1,      // Something was indexed beyond its bounds.
            SCEC_INVALID_INPUT = 2,     // User provided some otherwise-bad data.
            SCEC_MISSING_VALUE = 3,     // Some value was required but not provided.
            SCEC_EXISTING_VALUE = 4,    // Some value was provided where not allowed.
            SCEC_EXCEEDED_LIMIT = 5,    // Some arbitrary limit -- gas or otherwise -- was hit.
            SCEC_INVALID_ACTION = 6,    // Data was valid but action requested was not.
            SCEC_INTERNAL_ERROR = 7,    // The host detected an error in its own logic.
            SCEC_UNEXPECTED_TYPE = 8,   // Some type wasn't as expected.
            SCEC_UNEXPECTED_SIZE = 9    // Something's size wasn't as expected.
        };
    """

    SCEC_ARITH_DOMAIN = 0
    SCEC_INDEX_BOUNDS = 1
    SCEC_INVALID_INPUT = 2
    SCEC_MISSING_VALUE = 3
    SCEC_EXISTING_VALUE = 4
    SCEC_EXCEEDED_LIMIT = 5
    SCEC_INVALID_ACTION = 6
    SCEC_INTERNAL_ERROR = 7
    SCEC_UNEXPECTED_TYPE = 8
    SCEC_UNEXPECTED_SIZE = 9

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCErrorCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCErrorCode:
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
    def from_xdr(cls, xdr: str) -> SCErrorCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCErrorCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _SC_ERROR_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> SCErrorCode:
        return cls(_SC_ERROR_CODE_REVERSE_MAP[json_value])
