# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import TYPE_CHECKING, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sc_spec_type import SCSpecType

if TYPE_CHECKING:
    from .sc_spec_type_bytes_n import SCSpecTypeBytesN
    from .sc_spec_type_map import SCSpecTypeMap
    from .sc_spec_type_option import SCSpecTypeOption
    from .sc_spec_type_result import SCSpecTypeResult
    from .sc_spec_type_tuple import SCSpecTypeTuple
    from .sc_spec_type_udt import SCSpecTypeUDT
    from .sc_spec_type_vec import SCSpecTypeVec
__all__ = ["SCSpecTypeDef"]


class SCSpecTypeDef:
    """
    XDR Source Code::

        union SCSpecTypeDef switch (SCSpecType type)
        {
        case SC_SPEC_TYPE_VAL:
        case SC_SPEC_TYPE_BOOL:
        case SC_SPEC_TYPE_VOID:
        case SC_SPEC_TYPE_ERROR:
        case SC_SPEC_TYPE_U32:
        case SC_SPEC_TYPE_I32:
        case SC_SPEC_TYPE_U64:
        case SC_SPEC_TYPE_I64:
        case SC_SPEC_TYPE_TIMEPOINT:
        case SC_SPEC_TYPE_DURATION:
        case SC_SPEC_TYPE_U128:
        case SC_SPEC_TYPE_I128:
        case SC_SPEC_TYPE_U256:
        case SC_SPEC_TYPE_I256:
        case SC_SPEC_TYPE_BYTES:
        case SC_SPEC_TYPE_STRING:
        case SC_SPEC_TYPE_SYMBOL:
        case SC_SPEC_TYPE_ADDRESS:
        case SC_SPEC_TYPE_MUXED_ADDRESS:
            void;
        case SC_SPEC_TYPE_OPTION:
            SCSpecTypeOption option;
        case SC_SPEC_TYPE_RESULT:
            SCSpecTypeResult result;
        case SC_SPEC_TYPE_VEC:
            SCSpecTypeVec vec;
        case SC_SPEC_TYPE_MAP:
            SCSpecTypeMap map;
        case SC_SPEC_TYPE_TUPLE:
            SCSpecTypeTuple tuple;
        case SC_SPEC_TYPE_BYTES_N:
            SCSpecTypeBytesN bytesN;
        case SC_SPEC_TYPE_UDT:
            SCSpecTypeUDT udt;
        };
    """

    def __init__(
        self,
        type: SCSpecType,
        option: Optional[SCSpecTypeOption] = None,
        result: Optional[SCSpecTypeResult] = None,
        vec: Optional[SCSpecTypeVec] = None,
        map: Optional[SCSpecTypeMap] = None,
        tuple: Optional[SCSpecTypeTuple] = None,
        bytes_n: Optional[SCSpecTypeBytesN] = None,
        udt: Optional[SCSpecTypeUDT] = None,
    ) -> None:
        self.type = type
        self.option = option
        self.result = result
        self.vec = vec
        self.map = map
        self.tuple = tuple
        self.bytes_n = bytes_n
        self.udt = udt

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCSpecType.SC_SPEC_TYPE_VAL:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_BOOL:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_VOID:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_ERROR:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_U32:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_I32:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_U64:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_I64:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_TIMEPOINT:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_DURATION:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_U128:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_I128:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_U256:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_I256:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_BYTES:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_STRING:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_SYMBOL:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_ADDRESS:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_MUXED_ADDRESS:
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_OPTION:
            if self.option is None:
                raise ValueError("option should not be None.")
            self.option.pack(packer)
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_RESULT:
            if self.result is None:
                raise ValueError("result should not be None.")
            self.result.pack(packer)
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_VEC:
            if self.vec is None:
                raise ValueError("vec should not be None.")
            self.vec.pack(packer)
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_MAP:
            if self.map is None:
                raise ValueError("map should not be None.")
            self.map.pack(packer)
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_TUPLE:
            if self.tuple is None:
                raise ValueError("tuple should not be None.")
            self.tuple.pack(packer)
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_BYTES_N:
            if self.bytes_n is None:
                raise ValueError("bytes_n should not be None.")
            self.bytes_n.pack(packer)
            return
        if self.type == SCSpecType.SC_SPEC_TYPE_UDT:
            if self.udt is None:
                raise ValueError("udt should not be None.")
            self.udt.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecTypeDef:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = SCSpecType.unpack(unpacker)
        if type == SCSpecType.SC_SPEC_TYPE_VAL:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_BOOL:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_VOID:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_ERROR:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_U32:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_I32:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_U64:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_I64:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_TIMEPOINT:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_DURATION:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_U128:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_I128:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_U256:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_I256:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_BYTES:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_STRING:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_SYMBOL:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_ADDRESS:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_MUXED_ADDRESS:
            return cls(type=type)
        if type == SCSpecType.SC_SPEC_TYPE_OPTION:
            from .sc_spec_type_option import SCSpecTypeOption

            option = SCSpecTypeOption.unpack(unpacker, depth_limit - 1)
            return cls(type=type, option=option)
        if type == SCSpecType.SC_SPEC_TYPE_RESULT:
            from .sc_spec_type_result import SCSpecTypeResult

            result = SCSpecTypeResult.unpack(unpacker, depth_limit - 1)
            return cls(type=type, result=result)
        if type == SCSpecType.SC_SPEC_TYPE_VEC:
            from .sc_spec_type_vec import SCSpecTypeVec

            vec = SCSpecTypeVec.unpack(unpacker, depth_limit - 1)
            return cls(type=type, vec=vec)
        if type == SCSpecType.SC_SPEC_TYPE_MAP:
            from .sc_spec_type_map import SCSpecTypeMap

            map = SCSpecTypeMap.unpack(unpacker, depth_limit - 1)
            return cls(type=type, map=map)
        if type == SCSpecType.SC_SPEC_TYPE_TUPLE:
            from .sc_spec_type_tuple import SCSpecTypeTuple

            tuple = SCSpecTypeTuple.unpack(unpacker, depth_limit - 1)
            return cls(type=type, tuple=tuple)
        if type == SCSpecType.SC_SPEC_TYPE_BYTES_N:
            from .sc_spec_type_bytes_n import SCSpecTypeBytesN

            bytes_n = SCSpecTypeBytesN.unpack(unpacker, depth_limit - 1)
            return cls(type=type, bytes_n=bytes_n)
        if type == SCSpecType.SC_SPEC_TYPE_UDT:
            from .sc_spec_type_udt import SCSpecTypeUDT

            udt = SCSpecTypeUDT.unpack(unpacker, depth_limit - 1)
            return cls(type=type, udt=udt)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecTypeDef:
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
    def from_xdr(cls, xdr: str) -> SCSpecTypeDef:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecTypeDef:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == SCSpecType.SC_SPEC_TYPE_VAL:
            return "val"
        if self.type == SCSpecType.SC_SPEC_TYPE_BOOL:
            return "bool"
        if self.type == SCSpecType.SC_SPEC_TYPE_VOID:
            return "void"
        if self.type == SCSpecType.SC_SPEC_TYPE_ERROR:
            return "error"
        if self.type == SCSpecType.SC_SPEC_TYPE_U32:
            return "u32"
        if self.type == SCSpecType.SC_SPEC_TYPE_I32:
            return "i32"
        if self.type == SCSpecType.SC_SPEC_TYPE_U64:
            return "u64"
        if self.type == SCSpecType.SC_SPEC_TYPE_I64:
            return "i64"
        if self.type == SCSpecType.SC_SPEC_TYPE_TIMEPOINT:
            return "timepoint"
        if self.type == SCSpecType.SC_SPEC_TYPE_DURATION:
            return "duration"
        if self.type == SCSpecType.SC_SPEC_TYPE_U128:
            return "u128"
        if self.type == SCSpecType.SC_SPEC_TYPE_I128:
            return "i128"
        if self.type == SCSpecType.SC_SPEC_TYPE_U256:
            return "u256"
        if self.type == SCSpecType.SC_SPEC_TYPE_I256:
            return "i256"
        if self.type == SCSpecType.SC_SPEC_TYPE_BYTES:
            return "bytes"
        if self.type == SCSpecType.SC_SPEC_TYPE_STRING:
            return "string"
        if self.type == SCSpecType.SC_SPEC_TYPE_SYMBOL:
            return "symbol"
        if self.type == SCSpecType.SC_SPEC_TYPE_ADDRESS:
            return "address"
        if self.type == SCSpecType.SC_SPEC_TYPE_MUXED_ADDRESS:
            return "muxed_address"
        if self.type == SCSpecType.SC_SPEC_TYPE_OPTION:
            assert self.option is not None
            return {"option": self.option.to_json_dict()}
        if self.type == SCSpecType.SC_SPEC_TYPE_RESULT:
            assert self.result is not None
            return {"result": self.result.to_json_dict()}
        if self.type == SCSpecType.SC_SPEC_TYPE_VEC:
            assert self.vec is not None
            return {"vec": self.vec.to_json_dict()}
        if self.type == SCSpecType.SC_SPEC_TYPE_MAP:
            assert self.map is not None
            return {"map": self.map.to_json_dict()}
        if self.type == SCSpecType.SC_SPEC_TYPE_TUPLE:
            assert self.tuple is not None
            return {"tuple": self.tuple.to_json_dict()}
        if self.type == SCSpecType.SC_SPEC_TYPE_BYTES_N:
            assert self.bytes_n is not None
            return {"bytes_n": self.bytes_n.to_json_dict()}
        if self.type == SCSpecType.SC_SPEC_TYPE_UDT:
            assert self.udt is not None
            return {"udt": self.udt.to_json_dict()}
        raise ValueError(f"Unknown type in SCSpecTypeDef: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> SCSpecTypeDef:
        if isinstance(json_value, str):
            if json_value not in (
                "val",
                "bool",
                "void",
                "error",
                "u32",
                "i32",
                "u64",
                "i64",
                "timepoint",
                "duration",
                "u128",
                "i128",
                "u256",
                "i256",
                "bytes",
                "string",
                "symbol",
                "address",
                "muxed_address",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for SCSpecTypeDef, must be one of: val, bool, void, error, u32, i32, u64, i64, timepoint, duration, u128, i128, u256, i256, bytes, string, symbol, address, muxed_address"
                )
            type = SCSpecType.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SCSpecTypeDef, got: {json_value}"
            )
        key = next(iter(json_value))
        type = SCSpecType.from_json_dict(key)
        if key == "option":
            from .sc_spec_type_option import SCSpecTypeOption

            option = SCSpecTypeOption.from_json_dict(json_value["option"])
            return cls(type=type, option=option)
        if key == "result":
            from .sc_spec_type_result import SCSpecTypeResult

            result = SCSpecTypeResult.from_json_dict(json_value["result"])
            return cls(type=type, result=result)
        if key == "vec":
            from .sc_spec_type_vec import SCSpecTypeVec

            vec = SCSpecTypeVec.from_json_dict(json_value["vec"])
            return cls(type=type, vec=vec)
        if key == "map":
            from .sc_spec_type_map import SCSpecTypeMap

            map_val = SCSpecTypeMap.from_json_dict(json_value["map"])
            return cls(type=type, map=map_val)
        if key == "tuple":
            from .sc_spec_type_tuple import SCSpecTypeTuple

            tuple = SCSpecTypeTuple.from_json_dict(json_value["tuple"])
            return cls(type=type, tuple=tuple)
        if key == "bytes_n":
            from .sc_spec_type_bytes_n import SCSpecTypeBytesN

            bytes_n = SCSpecTypeBytesN.from_json_dict(json_value["bytes_n"])
            return cls(type=type, bytes_n=bytes_n)
        if key == "udt":
            from .sc_spec_type_udt import SCSpecTypeUDT

            udt = SCSpecTypeUDT.from_json_dict(json_value["udt"])
            return cls(type=type, udt=udt)
        raise ValueError(f"Unknown key '{key}' for SCSpecTypeDef")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.option,
                self.result,
                self.vec,
                self.map,
                self.tuple,
                self.bytes_n,
                self.udt,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.option == other.option
            and self.result == other.result
            and self.vec == other.vec
            and self.map == other.map
            and self.tuple == other.tuple
            and self.bytes_n == other.bytes_n
            and self.udt == other.udt
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.option is not None:
            out.append(f"option={self.option}")
        if self.result is not None:
            out.append(f"result={self.result}")
        if self.vec is not None:
            out.append(f"vec={self.vec}")
        if self.map is not None:
            out.append(f"map={self.map}")
        if self.tuple is not None:
            out.append(f"tuple={self.tuple}")
        if self.bytes_n is not None:
            out.append(f"bytes_n={self.bytes_n}")
        if self.udt is not None:
            out.append(f"udt={self.udt}")
        return f"<SCSpecTypeDef [{', '.join(out)}]>"
