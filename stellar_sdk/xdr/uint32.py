# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, UnsignedInteger

__all__ = ["Uint32"]


class Uint32:
    """
    XDR Source Code::

        typedef unsigned int uint32;
    """

    def __init__(self, uint32: int) -> None:
        self.uint32 = uint32

    def pack(self, packer: Packer) -> None:
        UnsignedInteger(self.uint32).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Uint32:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        uint32 = UnsignedInteger.unpack(unpacker)
        return cls(uint32)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Uint32:
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
    def from_xdr(cls, xdr: str) -> Uint32:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Uint32:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return UnsignedInteger.to_json_dict(self.uint32)

    @classmethod
    def from_json_dict(cls, json_value: int) -> Uint32:
        return cls(UnsignedInteger.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.uint32,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint32 == other.uint32

    def __repr__(self):
        return f"<Uint32 [uint32={self.uint32}]>"
