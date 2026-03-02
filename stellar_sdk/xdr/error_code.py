# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_ERROR_CODE_MAP = {0: "misc", 1: "data", 2: "conf", 3: "auth", 4: "load"}
_ERROR_CODE_REVERSE_MAP = {"misc": 0, "data": 1, "conf": 2, "auth": 3, "load": 4}
__all__ = ["ErrorCode"]


class ErrorCode(IntEnum):
    """
    XDR Source Code::

        enum ErrorCode
        {
            ERR_MISC = 0, // Unspecific error
            ERR_DATA = 1, // Malformed data
            ERR_CONF = 2, // Misconfiguration error
            ERR_AUTH = 3, // Authentication failure
            ERR_LOAD = 4  // System overloaded
        };
    """

    ERR_MISC = 0
    ERR_DATA = 1
    ERR_CONF = 2
    ERR_AUTH = 3
    ERR_LOAD = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ErrorCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ErrorCode:
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
    def from_xdr(cls, xdr: str) -> ErrorCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ErrorCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _ERROR_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ErrorCode:
        return cls(_ERROR_CODE_REVERSE_MAP[json_value])
