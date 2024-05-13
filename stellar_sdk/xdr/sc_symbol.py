# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import String
from .constants import *

__all__ = ["SCSymbol"]


class SCSymbol:
    """
    XDR Source Code::

        typedef string SCSymbol<SCSYMBOL_LIMIT>;
    """

    def __init__(self, sc_symbol: bytes) -> None:
        self.sc_symbol = sc_symbol

    def pack(self, packer: Packer) -> None:
        String(self.sc_symbol, SCSYMBOL_LIMIT).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSymbol:
        sc_symbol = String.unpack(unpacker)
        return cls(sc_symbol)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSymbol:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSymbol:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.sc_symbol)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sc_symbol == other.sc_symbol

    def __repr__(self):
        return f"<SCSymbol [sc_symbol={self.sc_symbol}]>"
