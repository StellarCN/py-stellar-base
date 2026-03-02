# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_MANAGE_DATA_RESULT_CODE_MAP = {
    0: "success",
    -1: "not_supported_yet",
    -2: "name_not_found",
    -3: "low_reserve",
    -4: "invalid_name",
}
_MANAGE_DATA_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "not_supported_yet": -1,
    "name_not_found": -2,
    "low_reserve": -3,
    "invalid_name": -4,
}
__all__ = ["ManageDataResultCode"]


class ManageDataResultCode(IntEnum):
    """
    XDR Source Code::

        enum ManageDataResultCode
        {
            // codes considered as "success" for the operation
            MANAGE_DATA_SUCCESS = 0,
            // codes considered as "failure" for the operation
            MANAGE_DATA_NOT_SUPPORTED_YET =
                -1, // The network hasn't moved to this protocol change yet
            MANAGE_DATA_NAME_NOT_FOUND =
                -2, // Trying to remove a Data Entry that isn't there
            MANAGE_DATA_LOW_RESERVE = -3, // not enough funds to create a new Data Entry
            MANAGE_DATA_INVALID_NAME = -4 // Name not a valid string
        };
    """

    MANAGE_DATA_SUCCESS = 0
    MANAGE_DATA_NOT_SUPPORTED_YET = -1
    MANAGE_DATA_NAME_NOT_FOUND = -2
    MANAGE_DATA_LOW_RESERVE = -3
    MANAGE_DATA_INVALID_NAME = -4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ManageDataResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ManageDataResultCode:
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
    def from_xdr(cls, xdr: str) -> ManageDataResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ManageDataResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _MANAGE_DATA_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ManageDataResultCode:
        return cls(_MANAGE_DATA_RESULT_CODE_REVERSE_MAP[json_value])
