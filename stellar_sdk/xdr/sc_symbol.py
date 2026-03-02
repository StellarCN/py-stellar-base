# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String
from .constants import *

__all__ = ["SCSymbol"]


class SCSymbol:
    """
    XDR Source Code::

        typedef string SCSymbol<SCSYMBOL_LIMIT>;
    """

    def __init__(self, sc_symbol: bytes) -> None:
        _expect_max_length = SCSYMBOL_LIMIT
        if sc_symbol and len(sc_symbol) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `sc_symbol` should be {_expect_max_length}, but got {len(sc_symbol)}."
            )
        self.sc_symbol = sc_symbol

    def pack(self, packer: Packer) -> None:
        String(self.sc_symbol, SCSYMBOL_LIMIT).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSymbol:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        sc_symbol = String.unpack(unpacker, SCSYMBOL_LIMIT)
        return cls(sc_symbol)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSymbol:
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
    def from_xdr(cls, xdr: str) -> SCSymbol:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSymbol:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return String.to_json_dict(self.sc_symbol)

    @classmethod
    def from_json_dict(cls, json_value: str) -> SCSymbol:
        return cls(String.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.sc_symbol,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sc_symbol == other.sc_symbol

    def __repr__(self):
        return f"<SCSymbol [sc_symbol={self.sc_symbol}]>"
