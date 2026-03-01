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

from .uint512 import Uint512
from .opt_hash1 import OptHash1
from .int1 import Int1
__all__ = ['MyStruct']
class MyStruct:
    """
    XDR Source Code::

        struct MyStruct
        {
            uint512 field1;
            optHash1 field2;
            int1 field3;
            unsigned int field4;
            float field5;
            double field6;
            bool field7;
        };
    """
    def __init__(
        self,
        field1: Uint512,
        field2: OptHash1,
        field3: Int1,
        field4: int,
        field5: float,
        field6: float,
        field7: bool,
    ) -> None:
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3
        self.field4 = field4
        self.field5 = field5
        self.field6 = field6
        self.field7 = field7
    def pack(self, packer: Packer) -> None:
        self.field1.pack(packer)
        self.field2.pack(packer)
        self.field3.pack(packer)
        UnsignedInteger(self.field4).pack(packer)
        Float(self.field5).pack(packer)
        Double(self.field6).pack(packer)
        Boolean(self.field7).pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> MyStruct:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        field1 = Uint512.unpack(unpacker, depth_limit - 1)
        field2 = OptHash1.unpack(unpacker, depth_limit - 1)
        field3 = Int1.unpack(unpacker, depth_limit - 1)
        field4 = UnsignedInteger.unpack(unpacker)
        field5 = Float.unpack(unpacker)
        field6 = Double.unpack(unpacker)
        field7 = Boolean.unpack(unpacker)
        return cls(
            field1=field1,
            field2=field2,
            field3=field3,
            field4=field4,
            field5=field5,
            field6=field6,
            field7=field7,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MyStruct:
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
    def from_xdr(cls, xdr: str) -> MyStruct:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> MyStruct:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> dict:
        return {
            "field1": self.field1.to_json_dict(),
            "field2": self.field2.to_json_dict(),
            "field3": self.field3.to_json_dict(),
            "field4": UnsignedInteger.to_json_dict(self.field4),
            "field5": Float.to_json_dict(self.field5),
            "field6": Double.to_json_dict(self.field6),
            "field7": Boolean.to_json_dict(self.field7),
        }
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> MyStruct:
        field1 = Uint512.from_json_dict(json_dict["field1"])
        field2 = OptHash1.from_json_dict(json_dict["field2"])
        field3 = Int1.from_json_dict(json_dict["field3"])
        field4 = UnsignedInteger.from_json_dict(json_dict["field4"])
        field5 = Float.from_json_dict(json_dict["field5"])
        field6 = Double.from_json_dict(json_dict["field6"])
        field7 = Boolean.from_json_dict(json_dict["field7"])
        return cls(
            field1=field1,
            field2=field2,
            field3=field3,
            field4=field4,
            field5=field5,
            field6=field6,
            field7=field7,
        )
    def __hash__(self):
        return hash((self.field1, self.field2, self.field3, self.field4, self.field5, self.field6, self.field7,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.field1 == other.field1 and self.field2 == other.field2 and self.field3 == other.field3 and self.field4 == other.field4 and self.field5 == other.field5 and self.field6 == other.field6 and self.field7 == other.field7
    def __repr__(self):
        out = [
            f'field1={self.field1}',
            f'field2={self.field2}',
            f'field3={self.field3}',
            f'field4={self.field4}',
            f'field5={self.field5}',
            f'field6={self.field6}',
            f'field7={self.field7}',
        ]
        return f"<MyStruct [{', '.join(out)}]>"
