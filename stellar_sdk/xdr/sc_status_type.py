# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

__all__ = ["SCStatusType"]


class SCStatusType(IntEnum):
    """
    XDR Source Code::

        enum SCStatusType
        {
            SST_OK = 0,
            SST_UNKNOWN_ERROR = 1,
            SST_HOST_VALUE_ERROR = 2,
            SST_HOST_OBJECT_ERROR = 3,
            SST_HOST_FUNCTION_ERROR = 4,
            SST_HOST_STORAGE_ERROR = 5,
            SST_HOST_CONTEXT_ERROR = 6,
            SST_VM_ERROR = 7,
            SST_CONTRACT_ERROR = 8,
            SST_HOST_AUTH_ERROR = 9
            // TODO: add more
        };
    """

    SST_OK = 0
    SST_UNKNOWN_ERROR = 1
    SST_HOST_VALUE_ERROR = 2
    SST_HOST_OBJECT_ERROR = 3
    SST_HOST_FUNCTION_ERROR = 4
    SST_HOST_STORAGE_ERROR = 5
    SST_HOST_CONTEXT_ERROR = 6
    SST_VM_ERROR = 7
    SST_CONTRACT_ERROR = 8
    SST_HOST_AUTH_ERROR = 9

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCStatusType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCStatusType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCStatusType":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
