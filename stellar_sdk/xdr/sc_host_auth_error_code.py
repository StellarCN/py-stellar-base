# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

__all__ = ["SCHostAuthErrorCode"]


class SCHostAuthErrorCode(IntEnum):
    """
    XDR Source Code::

        enum SCHostAuthErrorCode
        {
            HOST_AUTH_UNKNOWN_ERROR = 0,
            HOST_AUTH_NONCE_ERROR = 1,
            HOST_AUTH_DUPLICATE_AUTHORIZATION = 2,
            HOST_AUTH_NOT_AUTHORIZED = 3
        };
    """

    HOST_AUTH_UNKNOWN_ERROR = 0
    HOST_AUTH_NONCE_ERROR = 1
    HOST_AUTH_DUPLICATE_AUTHORIZATION = 2
    HOST_AUTH_NOT_AUTHORIZED = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCHostAuthErrorCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCHostAuthErrorCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCHostAuthErrorCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
