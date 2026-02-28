# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import DEFAULT_XDR_MAX_DEPTH, Integer, UnsignedInteger, Float, Double, Hyper, UnsignedHyper, Boolean, String, Opaque
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
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> HasOptions:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        first_option = Integer.unpack(unpacker) if unpacker.unpack_uint() else None
        second_option = Integer.unpack(unpacker) if unpacker.unpack_uint() else None
        third_option = Arr.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> HasOptions:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HasOptions:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> dict:
        return {
            "first_option": Integer.to_json_dict(self.first_option) if self.first_option is not None else None,
            "second_option": Integer.to_json_dict(self.second_option) if self.second_option is not None else None,
            "third_option": self.third_option.to_json_dict() if self.third_option is not None else None,
        }
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> HasOptions:
        first_option = Integer.from_json_dict(json_dict["first_option"]) if json_dict["first_option"] is not None else None
        second_option = Integer.from_json_dict(json_dict["second_option"]) if json_dict["second_option"] is not None else None
        third_option = Arr.from_json_dict(json_dict["third_option"]) if json_dict["third_option"] is not None else None
        return cls(
            first_option=first_option,
            second_option=second_option,
            third_option=third_option,
        )
    def __hash__(self):
        return hash((self.first_option, self.second_option, self.third_option,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.first_option == other.first_option and self.second_option == other.second_option and self.third_option == other.third_option
    def __repr__(self):
        out = [
            f'first_option={self.first_option}',
            f'second_option={self.second_option}',
            f'third_option={self.third_option}',
        ]
        return f"<HasOptions [{', '.join(out)}]>"
