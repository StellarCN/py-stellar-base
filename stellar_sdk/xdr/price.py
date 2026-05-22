# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .int32 import Int32

__all__ = ["Price"]


class Price:
    """
    XDR Source Code::

        struct Price
        {
            int32 n; // numerator
            int32 d; // denominator
        };
    """

    def __init__(
        self,
        n: Int32,
        d: Int32,
    ) -> None:
        self.n = n
        self.d = d

    def pack(self, packer: Packer) -> None:
        self.n.pack(packer)
        self.d.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Price:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        n = Int32.unpack(unpacker, depth_limit - 1)
        d = Int32.unpack(unpacker, depth_limit - 1)
        return cls(
            n=n,
            d=d,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Price:
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
    def from_xdr(cls, xdr: str) -> Price:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Price:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "n": self.n.to_json_dict(),
            "d": self.d.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> Price:
        n = Int32.from_json_dict(json_dict["n"])
        d = Int32.from_json_dict(json_dict["d"])
        return cls(
            n=n,
            d=d,
        )

    def __hash__(self):
        return hash(
            (
                self.n,
                self.d,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.n == other.n and self.d == other.d

    def __repr__(self):
        out = [
            f"n={self.n}",
            f"d={self.d}",
        ]
        return f"<Price [{', '.join(out)}]>"
