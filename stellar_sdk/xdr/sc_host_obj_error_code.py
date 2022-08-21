# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

__all__ = ["SCHostObjErrorCode"]


class SCHostObjErrorCode(IntEnum):
    """
    XDR Source Code::

        enum SCHostObjErrorCode
        {
            HOST_OBJECT_UNKNOWN_ERROR = 0,
            HOST_OBJECT_UNKNOWN_REFERENCE = 1,
            HOST_OBJECT_UNEXPECTED_TYPE = 2,
            HOST_OBJECT_OBJECT_COUNT_EXCEEDS_U32_MAX = 3,
            HOST_OBJECT_OBJECT_NOT_EXIST = 4,
            HOST_OBJECT_VEC_INDEX_OUT_OF_BOUND = 5,
            HOST_OBJECT_CONTRACT_HASH_WRONG_LENGTH = 6
        };
    """

    HOST_OBJECT_UNKNOWN_ERROR = 0
    HOST_OBJECT_UNKNOWN_REFERENCE = 1
    HOST_OBJECT_UNEXPECTED_TYPE = 2
    HOST_OBJECT_OBJECT_COUNT_EXCEEDS_U32_MAX = 3
    HOST_OBJECT_OBJECT_NOT_EXIST = 4
    HOST_OBJECT_VEC_INDEX_OUT_OF_BOUND = 5
    HOST_OBJECT_CONTRACT_HASH_WRONG_LENGTH = 6

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCHostObjErrorCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCHostObjErrorCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCHostObjErrorCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
