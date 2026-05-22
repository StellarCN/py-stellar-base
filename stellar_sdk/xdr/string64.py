# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String

__all__ = ["String64"]


class String64:
    """
    XDR Source Code::

        typedef string string64<64>;
    """

    def __init__(self, string64: bytes) -> None:
        _expect_max_length = 64
        if string64 and len(string64) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `string64` should be {_expect_max_length}, but got {len(string64)}."
            )
        self.string64 = string64

    def pack(self, packer: Packer) -> None:
        String(self.string64, 64).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> String64:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        string64 = String.unpack(unpacker, 64)
        return cls(string64)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> String64:
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
    def from_xdr(cls, xdr: str) -> String64:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> String64:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return String.to_json_dict(self.string64)

    @classmethod
    def from_json_dict(cls, json_value: str) -> String64:
        return cls(String.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.string64,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.string64 == other.string64

    def __repr__(self):
        return f"<String64 [string64={self.string64}]>"
