# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_INVOKE_HOST_FUNCTION_RESULT_CODE_MAP = {
    0: "success",
    -1: "malformed",
    -2: "trapped",
    -3: "resource_limit_exceeded",
    -4: "entry_archived",
    -5: "insufficient_refundable_fee",
}
_INVOKE_HOST_FUNCTION_RESULT_CODE_REVERSE_MAP = {
    "success": 0,
    "malformed": -1,
    "trapped": -2,
    "resource_limit_exceeded": -3,
    "entry_archived": -4,
    "insufficient_refundable_fee": -5,
}
__all__ = ["InvokeHostFunctionResultCode"]


class InvokeHostFunctionResultCode(IntEnum):
    """
    XDR Source Code::

        enum InvokeHostFunctionResultCode
        {
            // codes considered as "success" for the operation
            INVOKE_HOST_FUNCTION_SUCCESS = 0,

            // codes considered as "failure" for the operation
            INVOKE_HOST_FUNCTION_MALFORMED = -1,
            INVOKE_HOST_FUNCTION_TRAPPED = -2,
            INVOKE_HOST_FUNCTION_RESOURCE_LIMIT_EXCEEDED = -3,
            INVOKE_HOST_FUNCTION_ENTRY_ARCHIVED = -4,
            INVOKE_HOST_FUNCTION_INSUFFICIENT_REFUNDABLE_FEE = -5
        };
    """

    INVOKE_HOST_FUNCTION_SUCCESS = 0
    INVOKE_HOST_FUNCTION_MALFORMED = -1
    INVOKE_HOST_FUNCTION_TRAPPED = -2
    INVOKE_HOST_FUNCTION_RESOURCE_LIMIT_EXCEEDED = -3
    INVOKE_HOST_FUNCTION_ENTRY_ARCHIVED = -4
    INVOKE_HOST_FUNCTION_INSUFFICIENT_REFUNDABLE_FEE = -5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> InvokeHostFunctionResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> InvokeHostFunctionResultCode:
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
    def from_xdr(cls, xdr: str) -> InvokeHostFunctionResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InvokeHostFunctionResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _INVOKE_HOST_FUNCTION_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> InvokeHostFunctionResultCode:
        return cls(_INVOKE_HOST_FUNCTION_RESULT_CODE_REVERSE_MAP[json_value])
