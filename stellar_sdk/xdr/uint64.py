# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, UnsignedHyper

__all__ = ["Uint64"]


class Uint64:
    """
    XDR Source Code::

        typedef unsigned hyper uint64;
    """

    def __init__(self, uint64: int) -> None:
        self.uint64 = uint64

    def pack(self, packer: Packer) -> None:
        UnsignedHyper(self.uint64).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Uint64:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        uint64 = UnsignedHyper.unpack(unpacker)
        return cls(uint64)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Uint64:
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
    def from_xdr(cls, xdr: str) -> Uint64:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Uint64:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return UnsignedHyper.to_json_dict(self.uint64)

    @classmethod
    def from_json_dict(cls, json_value: str) -> Uint64:
        return cls(UnsignedHyper.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.uint64,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint64 == other.uint64

    def __repr__(self):
        return f"<Uint64 [uint64={self.uint64}]>"
