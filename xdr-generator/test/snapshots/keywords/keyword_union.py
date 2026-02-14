# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .keyword_enum import KeywordEnum
from .pass_ import Pass
__all__ = ['KeywordUnion']
class KeywordUnion:
    """
    XDR Source Code::

        union keyword_union switch (keyword_enum from)
        {
            case from:
                pass class;
            default:
                void;
        };
    """
    def __init__(
        self,
        from_: KeywordEnum,
        class_: Optional[Pass] = None,
    ) -> None:
        self.from_ = from_
        self.class_ = class_
    def pack(self, packer: Packer) -> None:
        self.from_.pack(packer)
        if self.from_ == KeywordEnum.from_:
            if self.class_ is None:
                raise ValueError("class_ should not be None.")
            self.class_.pack(packer)
            return
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> KeywordUnion:
        from_ = KeywordEnum.unpack(unpacker)
        if from_ == KeywordEnum.from_:
            class_ = Pass.unpack(unpacker)
            return cls(from_=from_, class_=class_)
        return cls(from_=from_)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> KeywordUnion:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> KeywordUnion:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.from_, self.class_,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.from_ == other.from_ and self.class_ == other.class_
    def __repr__(self):
        out = []
        out.append(f'from_={self.from_}')
        if self.class_ is not None:
            out.append(f'class_={self.class_}')
        return f"<KeywordUnion [{', '.join(out)}]>"
