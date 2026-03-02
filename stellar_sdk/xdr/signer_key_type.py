# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_SIGNER_KEY_TYPE_MAP = {
    0: "ed25519",
    1: "pre_auth_tx",
    2: "hash_x",
    3: "ed25519_signed_payload",
}
_SIGNER_KEY_TYPE_REVERSE_MAP = {
    "ed25519": 0,
    "pre_auth_tx": 1,
    "hash_x": 2,
    "ed25519_signed_payload": 3,
}
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SignerKeyType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SignerKeyType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _SIGNER_KEY_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> SignerKeyType:
        return cls(_SIGNER_KEY_TYPE_REVERSE_MAP[json_value])
