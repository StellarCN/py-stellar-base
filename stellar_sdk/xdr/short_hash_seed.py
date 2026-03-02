# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["ShortHashSeed"]


class ShortHashSeed:
    """
    XDR Source Code::

        struct ShortHashSeed
        {
            opaque seed[16];
        };
    """

    def __init__(
        self,
        seed: bytes,
    ) -> None:
        _expect_length = 16
        if seed and len(seed) != _expect_length:
            raise ValueError(
                f"The length of `seed` should be {_expect_length}, but got {len(seed)}."
            )
        self.seed = seed

    def pack(self, packer: Packer) -> None:
        Opaque(self.seed, 16, True).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ShortHashSeed:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        seed = Opaque.unpack(unpacker, 16, True)
        return cls(
            seed=seed,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ShortHashSeed:
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
    def from_xdr(cls, xdr: str) -> ShortHashSeed:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ShortHashSeed:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "seed": Opaque.to_json_dict(self.seed),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ShortHashSeed:
        seed = Opaque.from_json_dict(json_dict["seed"])
        return cls(
            seed=seed,
        )

    def __hash__(self):
        return hash((self.seed,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.seed == other.seed

    def __repr__(self):
        out = [
            f"seed={self.seed}",
        ]
        return f"<ShortHashSeed [{', '.join(out)}]>"
