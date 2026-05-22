# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String

__all__ = ["SCString"]


class SCString:
    """
    XDR Source Code::

        typedef string SCString<>;
    """

    def __init__(self, sc_string: bytes) -> None:
        _expect_max_length = 4294967295
        if sc_string and len(sc_string) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `sc_string` should be {_expect_max_length}, but got {len(sc_string)}."
            )
        self.sc_string = sc_string

    def pack(self, packer: Packer) -> None:
        String(self.sc_string, 4294967295).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCString:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        sc_string = String.unpack(unpacker, 4294967295)
        return cls(sc_string)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCString:
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
    def from_xdr(cls, xdr: str) -> SCString:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCString:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return String.to_json_dict(self.sc_string)

    @classmethod
    def from_json_dict(cls, json_value: str) -> SCString:
        return cls(String.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.sc_string,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sc_string == other.sc_string

    def __repr__(self):
        return f"<SCString [sc_string={self.sc_string}]>"
