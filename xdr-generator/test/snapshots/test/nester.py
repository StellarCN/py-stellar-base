# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
from .constants import *

from .nester_nested_enum import NesterNestedEnum
from .nester_nested_struct import NesterNestedStruct
from .nester_nested_union import NesterNestedUnion
__all__ = ['Nester']
class Nester:
    """
    XDR Source Code::

        struct Nester
        {
          enum {
            BLAH_1,
            BLAH_2
          } nestedEnum;

          struct {
            int blah;
          } nestedStruct;

          union switch (Color color) {
            case RED:
              void;
            default:
              int blah2;
          } nestedUnion;


        };
    """
    def __init__(
        self,
        nested_enum: NesterNestedEnum,
        nested_struct: NesterNestedStruct,
        nested_union: NesterNestedUnion,
    ) -> None:
        self.nested_enum = nested_enum
        self.nested_struct = nested_struct
        self.nested_union = nested_union
    def pack(self, packer: Packer) -> None:
        self.nested_enum.pack(packer)
        self.nested_struct.pack(packer)
        self.nested_union.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Nester:
        nested_enum = NesterNestedEnum.unpack(unpacker)
        nested_struct = NesterNestedStruct.unpack(unpacker)
        nested_union = NesterNestedUnion.unpack(unpacker)
        return cls(
            nested_enum=nested_enum,
            nested_struct=nested_struct,
            nested_union=nested_union,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Nester:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Nester:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
    def __hash__(self):
        return hash((self.nested_enum, self.nested_struct, self.nested_union,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.nested_enum== other.nested_enum and self.nested_struct== other.nested_struct and self.nested_union== other.nested_union
    def __repr__(self):
        out = [
            f'nested_enum={self.nested_enum}',
            f'nested_struct={self.nested_struct}',
            f'nested_union={self.nested_union}',
        ]
        return f"<Nester [{', '.join(out)}]>"
