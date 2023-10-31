# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> InvokeHostFunctionResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
