# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String

__all__ = ["String32"]


class String32:
    """
    XDR Source Code::

        typedef string string32<32>;
    """

    def __init__(self, string32: bytes) -> None:
        _expect_max_length = 32
        if string32 and len(string32) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `string32` should be {_expect_max_length}, but got {len(string32)}."
            )
        self.string32 = string32

    def pack(self, packer: Packer) -> None:
        String(self.string32, 32).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> String32:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        string32 = String.unpack(unpacker, 32)
        return cls(string32)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> String32:
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
    def from_xdr(cls, xdr: str) -> String32:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> String32:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return String.to_json_dict(self.string32)

    @classmethod
    def from_json_dict(cls, json_value: str) -> String32:
        return cls(String.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.string32,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.string32 == other.string32

    def __repr__(self):
        return f"<String32 [string32={self.string32}]>"
