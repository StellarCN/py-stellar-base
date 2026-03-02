# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .signer_key import SignerKey
from .uint32 import Uint32

__all__ = ["Signer"]


class Signer:
    """
    XDR Source Code::

        struct Signer
        {
            SignerKey key;
            uint32 weight; // really only need 1 byte
        };
    """

    def __init__(
        self,
        key: SignerKey,
        weight: Uint32,
    ) -> None:
        self.key = key
        self.weight = weight

    def pack(self, packer: Packer) -> None:
        self.key.pack(packer)
        self.weight.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Signer:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        key = SignerKey.unpack(unpacker, depth_limit - 1)
        weight = Uint32.unpack(unpacker, depth_limit - 1)
        return cls(
            key=key,
            weight=weight,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Signer:
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
    def from_xdr(cls, xdr: str) -> Signer:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Signer:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "key": self.key.to_json_dict(),
            "weight": self.weight.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> Signer:
        key = SignerKey.from_json_dict(json_dict["key"])
        weight = Uint32.from_json_dict(json_dict["weight"])
        return cls(
            key=key,
            weight=weight,
        )

    def __hash__(self):
        return hash(
            (
                self.key,
                self.weight,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key and self.weight == other.weight

    def __repr__(self):
        out = [
            f"key={self.key}",
            f"weight={self.weight}",
        ]
        return f"<Signer [{', '.join(out)}]>"
