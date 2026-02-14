# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .pass_ import Pass
from .keyword_enum import KeywordEnum
__all__ = ['KeywordStruct']
class KeywordStruct:
    """
    XDR Source Code::

        struct keyword_struct {
          pass from;
          keyword_enum return;
        };
    """
    def __init__(
        self,
        from_: Pass,
        return_: KeywordEnum,
    ) -> None:
        self.from_ = from_
        self.return_ = return_
    def pack(self, packer: Packer) -> None:
        self.from_.pack(packer)
        self.return_.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> KeywordStruct:
        from_ = Pass.unpack(unpacker)
        return_ = KeywordEnum.unpack(unpacker)
        return cls(
            from_=from_,
            return_=return_,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> KeywordStruct:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> KeywordStruct:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.from_, self.return_,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.from_ == other.from_ and self.return_ == other.return_
    def __repr__(self):
        out = [
            f'from_={self.from_}',
            f'return_={self.return_}',
        ]
        return f"<KeywordStruct [{', '.join(out)}]>"
