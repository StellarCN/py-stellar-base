# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .error import Error
from .multi import Multi
__all__ = ['IntUnion']
class IntUnion:
    """
    XDR Source Code::

        union IntUnion switch (int type)
        {
            case 0:
                Error error;
            case 1:
                Multi things<>;

        };
    """
    def __init__(
        self,
        type: int,
        error: Optional[Error] = None,
        things: Optional[List[Multi]] = None,
    ) -> None:
        _expect_max_length = 4294967295
        if things and len(things) > _expect_max_length:
            raise ValueError(f"The maximum length of `things` should be {_expect_max_length}, but got {len(things)}.")
        self.type = type
        self.error = error
        self.things = things
    def pack(self, packer: Packer) -> None:
        Integer(self.type).pack(packer)
        if self.type == 0:
            if self.error is None:
                raise ValueError("error should not be None.")
            self.error.pack(packer)
            return
        if self.type == 1:
            if self.things is None:
                raise ValueError("things should not be None.")
            packer.pack_uint(len(self.things))
            for things_item in self.things:
                things_item.pack(packer)
            return
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> IntUnion:
        type = Integer.unpack(unpacker)
        if type == 0:
            error = Error.unpack(unpacker)
            return cls(type=type, error=error)
        if type == 1:
            length = unpacker.unpack_uint()
            things = []
            for _ in range(length):
                things.append(Multi.unpack(unpacker))
            return cls(type=type, things=things)
        return cls(type=type)
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> IntUnion:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> IntUnion:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.type, self.error, self.things,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type== other.type and self.error== other.error and self.things== other.things
    def __repr__(self):
        out = []
        out.append(f'type={self.type}')
        out.append(f'error={self.error}') if self.error is not None else None
        out.append(f'things={self.things}') if self.things is not None else None
        return f"<IntUnion [{', '.join(out)}]>"
