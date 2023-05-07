# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib3 import Packer, Unpacker

__all__ = ["SCStatic"]


class SCStatic(IntEnum):
    """
    XDR Source Code::

        enum SCStatic
        {
            SCS_VOID = 0,
            SCS_TRUE = 1,
            SCS_FALSE = 2,
            SCS_LEDGER_KEY_CONTRACT_CODE = 3
        };
    """

    SCS_VOID = 0
    SCS_TRUE = 1
    SCS_FALSE = 2
    SCS_LEDGER_KEY_CONTRACT_CODE = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCStatic":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCStatic":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCStatic":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
