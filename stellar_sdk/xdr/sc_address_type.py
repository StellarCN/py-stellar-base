# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["SCAddressType"]


class SCAddressType(IntEnum):
    """
    XDR Source Code::

        enum SCAddressType
        {
            SC_ADDRESS_TYPE_ACCOUNT = 0,
            SC_ADDRESS_TYPE_CONTRACT = 1,
            SC_ADDRESS_TYPE_MUXED_ACCOUNT = 2,
            SC_ADDRESS_TYPE_CLAIMABLE_BALANCE = 3,
            SC_ADDRESS_TYPE_LIQUIDITY_POOL = 4
        };
    """

    SC_ADDRESS_TYPE_ACCOUNT = 0
    SC_ADDRESS_TYPE_CONTRACT = 1
    SC_ADDRESS_TYPE_MUXED_ACCOUNT = 2
    SC_ADDRESS_TYPE_CLAIMABLE_BALANCE = 3
    SC_ADDRESS_TYPE_LIQUIDITY_POOL = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCAddressType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCAddressType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCAddressType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
