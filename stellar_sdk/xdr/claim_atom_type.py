# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

__all__ = ["ClaimAtomType"]


class ClaimAtomType(IntEnum):
    """
    XDR Source Code::

        enum ClaimAtomType
        {
            CLAIM_ATOM_TYPE_V0 = 0,
            CLAIM_ATOM_TYPE_ORDER_BOOK = 1,
            CLAIM_ATOM_TYPE_LIQUIDITY_POOL = 2
        };
    """

    CLAIM_ATOM_TYPE_V0 = 0
    CLAIM_ATOM_TYPE_ORDER_BOOK = 1
    CLAIM_ATOM_TYPE_LIQUIDITY_POOL = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClaimAtomType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ClaimAtomType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClaimAtomType":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
