# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

__all__ = ["SCObjectType"]


class SCObjectType(IntEnum):
    """
    XDR Source Code::

        enum SCObjectType
        {
            // We have a few objects that represent non-stellar-specific concepts
            // like general-purpose maps, vectors, numbers, blobs.

            SCO_VEC = 0,
            SCO_MAP = 1,
            SCO_U64 = 2,
            SCO_I64 = 3,
            SCO_U128 = 4,
            SCO_I128 = 5,
            SCO_BYTES = 6,
            SCO_CONTRACT_CODE = 7,
            SCO_ADDRESS = 8,
            SCO_NONCE_KEY = 9

            // TODO: add more
        };
    """

    SCO_VEC = 0
    SCO_MAP = 1
    SCO_U64 = 2
    SCO_I64 = 3
    SCO_U128 = 4
    SCO_I128 = 5
    SCO_BYTES = 6
    SCO_CONTRACT_CODE = 7
    SCO_ADDRESS = 8
    SCO_NONCE_KEY = 9

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCObjectType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCObjectType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCObjectType":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
