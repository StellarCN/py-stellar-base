# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["Curve25519Secret"]


class Curve25519Secret:
    """
    XDR Source Code::

        struct Curve25519Secret
        {
            opaque key[32];
        };
    """

    def __init__(
        self,
        key: bytes,
    ) -> None:
        _expect_length = 32
        if key and len(key) != _expect_length:
            raise ValueError(
                f"The length of `key` should be {_expect_length}, but got {len(key)}."
            )
        self.key = key

    def pack(self, packer: Packer) -> None:
        Opaque(self.key, 32, True).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Curve25519Secret:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        key = Opaque.unpack(unpacker, 32, True)
        return cls(
            key=key,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Curve25519Secret:
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
    def from_xdr(cls, xdr: str) -> Curve25519Secret:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Curve25519Secret:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "key": Opaque.to_json_dict(self.key),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> Curve25519Secret:
        key = Opaque.from_json_dict(json_dict["key"])
        return cls(
            key=key,
        )

    def __hash__(self):
        return hash((self.key,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key

    def __repr__(self):
        out = [
            f"key={self.key}",
        ]
        return f"<Curve25519Secret [{', '.join(out)}]>"
