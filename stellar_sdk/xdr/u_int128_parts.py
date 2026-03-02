# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .uint64 import Uint64

__all__ = ["UInt128Parts"]


class UInt128Parts:
    """
    XDR Source Code::

        struct UInt128Parts {
            uint64 hi;
            uint64 lo;
        };
    """

    def __init__(
        self,
        hi: Uint64,
        lo: Uint64,
    ) -> None:
        self.hi = hi
        self.lo = lo

    def pack(self, packer: Packer) -> None:
        self.hi.pack(packer)
        self.lo.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> UInt128Parts:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        hi = Uint64.unpack(unpacker, depth_limit - 1)
        lo = Uint64.unpack(unpacker, depth_limit - 1)
        return cls(
            hi=hi,
            lo=lo,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> UInt128Parts:
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
    def from_xdr(cls, xdr: str) -> UInt128Parts:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> UInt128Parts:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        value_bytes = self.hi.uint64.to_bytes(
            8, "big", signed=False
        ) + self.lo.uint64.to_bytes(8, "big", signed=False)
        return str(int.from_bytes(value_bytes, "big", signed=False))

    @classmethod
    def from_json_dict(cls, json_value: str) -> UInt128Parts:
        from .uint64 import Uint64

        value_bytes = int(json_value).to_bytes(16, "big", signed=False)
        return cls(
            hi=Uint64(int.from_bytes(value_bytes[0:8], "big", signed=False)),
            lo=Uint64(int.from_bytes(value_bytes[8:16], "big", signed=False)),
        )

    def __hash__(self):
        return hash(
            (
                self.hi,
                self.lo,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hi == other.hi and self.lo == other.lo

    def __repr__(self):
        out = [
            f"hi={self.hi}",
            f"lo={self.lo}",
        ]
        return f"<UInt128Parts [{', '.join(out)}]>"
