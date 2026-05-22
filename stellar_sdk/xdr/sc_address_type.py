# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_SC_ADDRESS_TYPE_MAP = {
    0: "account",
    1: "contract",
    2: "muxed_account",
    3: "claimable_balance",
    4: "liquidity_pool",
}
_SC_ADDRESS_TYPE_REVERSE_MAP = {
    "account": 0,
    "contract": 1,
    "muxed_account": 2,
    "claimable_balance": 3,
    "liquidity_pool": 4,
}
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCAddressType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCAddressType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _SC_ADDRESS_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> SCAddressType:
        return cls(_SC_ADDRESS_TYPE_REVERSE_MAP[json_value])
