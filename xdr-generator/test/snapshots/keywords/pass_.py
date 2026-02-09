# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

__all__ = ['Pass']
class Pass:
    """
    XDR Source Code::

        typedef int pass;
    """
    def __init__(self, pass_: int) -> None:
        self.pass_ = pass_
    def pack(self, packer: Packer) -> None:
        Integer(self.pass_).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Pass:
        pass_ = Integer.unpack(unpacker)
        return cls(pass_)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Pass:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Pass:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash(self.pass_)
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.pass_ == other.pass_

    def __repr__(self):
        return f"<Pass [pass_={self.pass_}]>"
