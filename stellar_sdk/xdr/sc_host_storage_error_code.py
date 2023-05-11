# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib3 import Packer, Unpacker

__all__ = ["SCHostStorageErrorCode"]


class SCHostStorageErrorCode(IntEnum):
    """
    XDR Source Code::

        enum SCHostStorageErrorCode
        {
            HOST_STORAGE_UNKNOWN_ERROR = 0,
            HOST_STORAGE_EXPECT_CONTRACT_DATA = 1,
            HOST_STORAGE_READWRITE_ACCESS_TO_READONLY_ENTRY = 2,
            HOST_STORAGE_ACCESS_TO_UNKNOWN_ENTRY = 3,
            HOST_STORAGE_MISSING_KEY_IN_GET = 4,
            HOST_STORAGE_GET_ON_DELETED_KEY = 5
        };
    """

    HOST_STORAGE_UNKNOWN_ERROR = 0
    HOST_STORAGE_EXPECT_CONTRACT_DATA = 1
    HOST_STORAGE_READWRITE_ACCESS_TO_READONLY_ENTRY = 2
    HOST_STORAGE_ACCESS_TO_UNKNOWN_ENTRY = 3
    HOST_STORAGE_MISSING_KEY_IN_GET = 4
    HOST_STORAGE_GET_ON_DELETED_KEY = 5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCHostStorageErrorCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCHostStorageErrorCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCHostStorageErrorCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
