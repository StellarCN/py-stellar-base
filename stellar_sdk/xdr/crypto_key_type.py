# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["CryptoKeyType"]


class CryptoKeyType(IntEnum):
    """
    XDR Source Code::

        enum CryptoKeyType
        {
            KEY_TYPE_ED25519 = 0,
            KEY_TYPE_PRE_AUTH_TX = 1,
            KEY_TYPE_HASH_X = 2,
            KEY_TYPE_ED25519_SIGNED_PAYLOAD = 3,
            // MUXED enum values for supported type are derived from the enum values
            // above by ORing them with 0x100
            KEY_TYPE_MUXED_ED25519 = 0x100
        };
    """

    KEY_TYPE_ED25519 = 0
    KEY_TYPE_PRE_AUTH_TX = 1
    KEY_TYPE_HASH_X = 2
    KEY_TYPE_ED25519_SIGNED_PAYLOAD = 3
    KEY_TYPE_MUXED_ED25519 = 256

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> CryptoKeyType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> CryptoKeyType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> CryptoKeyType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
