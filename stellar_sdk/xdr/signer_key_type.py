# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

__all__ = ["SignerKeyType"]


class SignerKeyType(IntEnum):
    """
    XDR Source Code::

        enum SignerKeyType
        {
            SIGNER_KEY_TYPE_ED25519 = KEY_TYPE_ED25519,
            SIGNER_KEY_TYPE_PRE_AUTH_TX = KEY_TYPE_PRE_AUTH_TX,
            SIGNER_KEY_TYPE_HASH_X = KEY_TYPE_HASH_X,
            SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD = KEY_TYPE_ED25519_SIGNED_PAYLOAD
        };
    """

    SIGNER_KEY_TYPE_ED25519 = 0
    SIGNER_KEY_TYPE_PRE_AUTH_TX = 1
    SIGNER_KEY_TYPE_HASH_X = 2
    SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SignerKeyType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SignerKeyType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignerKeyType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
