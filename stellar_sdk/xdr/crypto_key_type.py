# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_CRYPTO_KEY_TYPE_MAP = {
    0: "ed25519",
    1: "pre_auth_tx",
    2: "hash_x",
    3: "ed25519_signed_payload",
    256: "muxed_ed25519",
}
_CRYPTO_KEY_TYPE_REVERSE_MAP = {
    "ed25519": 0,
    "pre_auth_tx": 1,
    "hash_x": 2,
    "ed25519_signed_payload": 3,
    "muxed_ed25519": 256,
}
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> CryptoKeyType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CryptoKeyType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _CRYPTO_KEY_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> CryptoKeyType:
        return cls(_CRYPTO_KEY_TYPE_REVERSE_MAP[json_value])
