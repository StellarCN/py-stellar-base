# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib3 import Packer, Unpacker

__all__ = ["SCHostFnErrorCode"]


class SCHostFnErrorCode(IntEnum):
    """
    XDR Source Code::

        enum SCHostFnErrorCode
        {
            HOST_FN_UNKNOWN_ERROR = 0,
            HOST_FN_UNEXPECTED_HOST_FUNCTION_ACTION = 1,
            HOST_FN_INPUT_ARGS_WRONG_LENGTH = 2,
            HOST_FN_INPUT_ARGS_WRONG_TYPE = 3,
            HOST_FN_INPUT_ARGS_INVALID = 4
        };
    """

    HOST_FN_UNKNOWN_ERROR = 0
    HOST_FN_UNEXPECTED_HOST_FUNCTION_ACTION = 1
    HOST_FN_INPUT_ARGS_WRONG_LENGTH = 2
    HOST_FN_INPUT_ARGS_WRONG_TYPE = 3
    HOST_FN_INPUT_ARGS_INVALID = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCHostFnErrorCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCHostFnErrorCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCHostFnErrorCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
