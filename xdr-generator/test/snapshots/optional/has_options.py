# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .arr import Arr
__all__ = ['HasOptions']
class HasOptions:
    """
    XDR Source Code::

        struct HasOptions
        {
          int* firstOption;
          int *secondOption;
          Arr *thirdOption;
        };
    """
    def __init__(
        self,
        first_option: Optional[int],
        second_option: Optional[int],
        third_option: Optional[Arr],
    ) -> None:
        self.first_option = first_option
        self.second_option = second_option
        self.third_option = third_option
    def pack(self, packer: Packer) -> None:
        if self.first_option is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            Integer(self.first_option).pack(packer)
        if self.second_option is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            Integer(self.second_option).pack(packer)
        if self.third_option is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.third_option.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> HasOptions:
        first_option = Integer.unpack(unpacker) if unpacker.unpack_uint() else None
        second_option = Integer.unpack(unpacker) if unpacker.unpack_uint() else None
        third_option = Arr.unpack(unpacker) if unpacker.unpack_uint() else None
        return cls(
            first_option=first_option,
            second_option=second_option,
            third_option=third_option,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HasOptions:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> HasOptions:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.first_option, self.second_option, self.third_option,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.first_option== other.first_option and self.second_option== other.second_option and self.third_option== other.third_option
    def __repr__(self):
        out = [
            f'first_option={self.first_option}',
            f'second_option={self.second_option}',
            f'third_option={self.third_option}',
        ]
        return f"<HasOptions [{', '.join(out)}]>"
