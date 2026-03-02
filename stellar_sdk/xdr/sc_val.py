# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import TYPE_CHECKING, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Boolean
from .sc_val_type import SCValType

if TYPE_CHECKING:
    from .duration import Duration
    from .int32 import Int32
    from .int64 import Int64
    from .int128_parts import Int128Parts
    from .int256_parts import Int256Parts
    from .sc_address import SCAddress
    from .sc_bytes import SCBytes
    from .sc_contract_instance import SCContractInstance
    from .sc_error import SCError
    from .sc_map import SCMap
    from .sc_nonce_key import SCNonceKey
    from .sc_string import SCString
    from .sc_symbol import SCSymbol
    from .sc_vec import SCVec
    from .time_point import TimePoint
    from .u_int128_parts import UInt128Parts
    from .u_int256_parts import UInt256Parts
    from .uint32 import Uint32
    from .uint64 import Uint64
__all__ = ["SCVal"]


class SCVal:
    """
    XDR Source Code::

        union SCVal switch (SCValType type)
        {

        case SCV_BOOL:
            bool b;
        case SCV_VOID:
            void;
        case SCV_ERROR:
            SCError error;

        case SCV_U32:
            uint32 u32;
        case SCV_I32:
            int32 i32;

        case SCV_U64:
            uint64 u64;
        case SCV_I64:
            int64 i64;
        case SCV_TIMEPOINT:
            TimePoint timepoint;
        case SCV_DURATION:
            Duration duration;

        case SCV_U128:
            UInt128Parts u128;
        case SCV_I128:
            Int128Parts i128;

        case SCV_U256:
            UInt256Parts u256;
        case SCV_I256:
            Int256Parts i256;

        case SCV_BYTES:
            SCBytes bytes;
        case SCV_STRING:
            SCString str;
        case SCV_SYMBOL:
            SCSymbol sym;

        // Vec and Map are recursive so need to live
        // behind an option, due to xdrpp limitations.
        case SCV_VEC:
            SCVec *vec;
        case SCV_MAP:
            SCMap *map;

        case SCV_ADDRESS:
            SCAddress address;

        // Special SCVals reserved for system-constructed contract-data
        // ledger keys, not generally usable elsewhere.
        case SCV_CONTRACT_INSTANCE:
            SCContractInstance instance;
        case SCV_LEDGER_KEY_CONTRACT_INSTANCE:
            void;
        case SCV_LEDGER_KEY_NONCE:
            SCNonceKey nonce_key;
        };
    """

    def __init__(
        self,
        type: SCValType,
        b: Optional[bool] = None,
        error: Optional[SCError] = None,
        u32: Optional[Uint32] = None,
        i32: Optional[Int32] = None,
        u64: Optional[Uint64] = None,
        i64: Optional[Int64] = None,
        timepoint: Optional[TimePoint] = None,
        duration: Optional[Duration] = None,
        u128: Optional[UInt128Parts] = None,
        i128: Optional[Int128Parts] = None,
        u256: Optional[UInt256Parts] = None,
        i256: Optional[Int256Parts] = None,
        bytes: Optional[SCBytes] = None,
        str: Optional[SCString] = None,
        sym: Optional[SCSymbol] = None,
        vec: Optional[Optional[SCVec]] = None,
        map: Optional[Optional[SCMap]] = None,
        address: Optional[SCAddress] = None,
        instance: Optional[SCContractInstance] = None,
        nonce_key: Optional[SCNonceKey] = None,
    ) -> None:
        self.type = type
        self.b = b
        self.error = error
        self.u32 = u32
        self.i32 = i32
        self.u64 = u64
        self.i64 = i64
        self.timepoint = timepoint
        self.duration = duration
        self.u128 = u128
        self.i128 = i128
        self.u256 = u256
        self.i256 = i256
        self.bytes = bytes
        self.str = str
        self.sym = sym
        self.vec = vec
        self.map = map
        self.address = address
        self.instance = instance
        self.nonce_key = nonce_key

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCValType.SCV_BOOL:
            if self.b is None:
                raise ValueError("b should not be None.")
            Boolean(self.b).pack(packer)
            return
        if self.type == SCValType.SCV_VOID:
            return
        if self.type == SCValType.SCV_ERROR:
            if self.error is None:
                raise ValueError("error should not be None.")
            self.error.pack(packer)
            return
        if self.type == SCValType.SCV_U32:
            if self.u32 is None:
                raise ValueError("u32 should not be None.")
            self.u32.pack(packer)
            return
        if self.type == SCValType.SCV_I32:
            if self.i32 is None:
                raise ValueError("i32 should not be None.")
            self.i32.pack(packer)
            return
        if self.type == SCValType.SCV_U64:
            if self.u64 is None:
                raise ValueError("u64 should not be None.")
            self.u64.pack(packer)
            return
        if self.type == SCValType.SCV_I64:
            if self.i64 is None:
                raise ValueError("i64 should not be None.")
            self.i64.pack(packer)
            return
        if self.type == SCValType.SCV_TIMEPOINT:
            if self.timepoint is None:
                raise ValueError("timepoint should not be None.")
            self.timepoint.pack(packer)
            return
        if self.type == SCValType.SCV_DURATION:
            if self.duration is None:
                raise ValueError("duration should not be None.")
            self.duration.pack(packer)
            return
        if self.type == SCValType.SCV_U128:
            if self.u128 is None:
                raise ValueError("u128 should not be None.")
            self.u128.pack(packer)
            return
        if self.type == SCValType.SCV_I128:
            if self.i128 is None:
                raise ValueError("i128 should not be None.")
            self.i128.pack(packer)
            return
        if self.type == SCValType.SCV_U256:
            if self.u256 is None:
                raise ValueError("u256 should not be None.")
            self.u256.pack(packer)
            return
        if self.type == SCValType.SCV_I256:
            if self.i256 is None:
                raise ValueError("i256 should not be None.")
            self.i256.pack(packer)
            return
        if self.type == SCValType.SCV_BYTES:
            if self.bytes is None:
                raise ValueError("bytes should not be None.")
            self.bytes.pack(packer)
            return
        if self.type == SCValType.SCV_STRING:
            if self.str is None:
                raise ValueError("str should not be None.")
            self.str.pack(packer)
            return
        if self.type == SCValType.SCV_SYMBOL:
            if self.sym is None:
                raise ValueError("sym should not be None.")
            self.sym.pack(packer)
            return
        if self.type == SCValType.SCV_VEC:
            if self.vec is None:
                packer.pack_uint(0)
            else:
                packer.pack_uint(1)
                if self.vec is None:
                    raise ValueError("vec should not be None.")
                self.vec.pack(packer)
            return
        if self.type == SCValType.SCV_MAP:
            if self.map is None:
                packer.pack_uint(0)
            else:
                packer.pack_uint(1)
                if self.map is None:
                    raise ValueError("map should not be None.")
                self.map.pack(packer)
            return
        if self.type == SCValType.SCV_ADDRESS:
            if self.address is None:
                raise ValueError("address should not be None.")
            self.address.pack(packer)
            return
        if self.type == SCValType.SCV_CONTRACT_INSTANCE:
            if self.instance is None:
                raise ValueError("instance should not be None.")
            self.instance.pack(packer)
            return
        if self.type == SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE:
            return
        if self.type == SCValType.SCV_LEDGER_KEY_NONCE:
            if self.nonce_key is None:
                raise ValueError("nonce_key should not be None.")
            self.nonce_key.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCVal:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = SCValType.unpack(unpacker)
        if type == SCValType.SCV_BOOL:
            b = Boolean.unpack(unpacker)
            return cls(type=type, b=b)
        if type == SCValType.SCV_VOID:
            return cls(type=type)
        if type == SCValType.SCV_ERROR:
            from .sc_error import SCError

            error = SCError.unpack(unpacker, depth_limit - 1)
            return cls(type=type, error=error)
        if type == SCValType.SCV_U32:
            from .uint32 import Uint32

            u32 = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(type=type, u32=u32)
        if type == SCValType.SCV_I32:
            from .int32 import Int32

            i32 = Int32.unpack(unpacker, depth_limit - 1)
            return cls(type=type, i32=i32)
        if type == SCValType.SCV_U64:
            from .uint64 import Uint64

            u64 = Uint64.unpack(unpacker, depth_limit - 1)
            return cls(type=type, u64=u64)
        if type == SCValType.SCV_I64:
            from .int64 import Int64

            i64 = Int64.unpack(unpacker, depth_limit - 1)
            return cls(type=type, i64=i64)
        if type == SCValType.SCV_TIMEPOINT:
            from .time_point import TimePoint

            timepoint = TimePoint.unpack(unpacker, depth_limit - 1)
            return cls(type=type, timepoint=timepoint)
        if type == SCValType.SCV_DURATION:
            from .duration import Duration

            duration = Duration.unpack(unpacker, depth_limit - 1)
            return cls(type=type, duration=duration)
        if type == SCValType.SCV_U128:
            from .u_int128_parts import UInt128Parts

            u128 = UInt128Parts.unpack(unpacker, depth_limit - 1)
            return cls(type=type, u128=u128)
        if type == SCValType.SCV_I128:
            from .int128_parts import Int128Parts

            i128 = Int128Parts.unpack(unpacker, depth_limit - 1)
            return cls(type=type, i128=i128)
        if type == SCValType.SCV_U256:
            from .u_int256_parts import UInt256Parts

            u256 = UInt256Parts.unpack(unpacker, depth_limit - 1)
            return cls(type=type, u256=u256)
        if type == SCValType.SCV_I256:
            from .int256_parts import Int256Parts

            i256 = Int256Parts.unpack(unpacker, depth_limit - 1)
            return cls(type=type, i256=i256)
        if type == SCValType.SCV_BYTES:
            from .sc_bytes import SCBytes

            bytes = SCBytes.unpack(unpacker, depth_limit - 1)
            return cls(type=type, bytes=bytes)
        if type == SCValType.SCV_STRING:
            from .sc_string import SCString

            str = SCString.unpack(unpacker, depth_limit - 1)
            return cls(type=type, str=str)
        if type == SCValType.SCV_SYMBOL:
            from .sc_symbol import SCSymbol

            sym = SCSymbol.unpack(unpacker, depth_limit - 1)
            return cls(type=type, sym=sym)
        if type == SCValType.SCV_VEC:
            from .sc_vec import SCVec

            vec = (
                SCVec.unpack(unpacker, depth_limit - 1)
                if unpacker.unpack_uint()
                else None
            )
            return cls(type=type, vec=vec)
        if type == SCValType.SCV_MAP:
            from .sc_map import SCMap

            map = (
                SCMap.unpack(unpacker, depth_limit - 1)
                if unpacker.unpack_uint()
                else None
            )
            return cls(type=type, map=map)
        if type == SCValType.SCV_ADDRESS:
            from .sc_address import SCAddress

            address = SCAddress.unpack(unpacker, depth_limit - 1)
            return cls(type=type, address=address)
        if type == SCValType.SCV_CONTRACT_INSTANCE:
            from .sc_contract_instance import SCContractInstance

            instance = SCContractInstance.unpack(unpacker, depth_limit - 1)
            return cls(type=type, instance=instance)
        if type == SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE:
            return cls(type=type)
        if type == SCValType.SCV_LEDGER_KEY_NONCE:
            from .sc_nonce_key import SCNonceKey

            nonce_key = SCNonceKey.unpack(unpacker, depth_limit - 1)
            return cls(type=type, nonce_key=nonce_key)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCVal:
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
    def from_xdr(cls, xdr: str) -> SCVal:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCVal:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == SCValType.SCV_BOOL:
            assert self.b is not None
            return {"bool": Boolean.to_json_dict(self.b)}
        if self.type == SCValType.SCV_VOID:
            return "void"
        if self.type == SCValType.SCV_ERROR:
            assert self.error is not None
            return {"error": self.error.to_json_dict()}
        if self.type == SCValType.SCV_U32:
            assert self.u32 is not None
            return {"u32": self.u32.to_json_dict()}
        if self.type == SCValType.SCV_I32:
            assert self.i32 is not None
            return {"i32": self.i32.to_json_dict()}
        if self.type == SCValType.SCV_U64:
            assert self.u64 is not None
            return {"u64": self.u64.to_json_dict()}
        if self.type == SCValType.SCV_I64:
            assert self.i64 is not None
            return {"i64": self.i64.to_json_dict()}
        if self.type == SCValType.SCV_TIMEPOINT:
            assert self.timepoint is not None
            return {"timepoint": self.timepoint.to_json_dict()}
        if self.type == SCValType.SCV_DURATION:
            assert self.duration is not None
            return {"duration": self.duration.to_json_dict()}
        if self.type == SCValType.SCV_U128:
            assert self.u128 is not None
            return {"u128": self.u128.to_json_dict()}
        if self.type == SCValType.SCV_I128:
            assert self.i128 is not None
            return {"i128": self.i128.to_json_dict()}
        if self.type == SCValType.SCV_U256:
            assert self.u256 is not None
            return {"u256": self.u256.to_json_dict()}
        if self.type == SCValType.SCV_I256:
            assert self.i256 is not None
            return {"i256": self.i256.to_json_dict()}
        if self.type == SCValType.SCV_BYTES:
            assert self.bytes is not None
            return {"bytes": self.bytes.to_json_dict()}
        if self.type == SCValType.SCV_STRING:
            assert self.str is not None
            return {"string": self.str.to_json_dict()}
        if self.type == SCValType.SCV_SYMBOL:
            assert self.sym is not None
            return {"symbol": self.sym.to_json_dict()}
        if self.type == SCValType.SCV_VEC:
            assert self.vec is not None
            return {"vec": self.vec.to_json_dict()}
        if self.type == SCValType.SCV_MAP:
            assert self.map is not None
            return {"map": self.map.to_json_dict()}
        if self.type == SCValType.SCV_ADDRESS:
            assert self.address is not None
            return {"address": self.address.to_json_dict()}
        if self.type == SCValType.SCV_CONTRACT_INSTANCE:
            assert self.instance is not None
            return {"contract_instance": self.instance.to_json_dict()}
        if self.type == SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE:
            return "ledger_key_contract_instance"
        if self.type == SCValType.SCV_LEDGER_KEY_NONCE:
            assert self.nonce_key is not None
            return {"ledger_key_nonce": self.nonce_key.to_json_dict()}
        raise ValueError(f"Unknown type in SCVal: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> SCVal:
        if isinstance(json_value, str):
            if json_value not in (
                "void",
                "ledger_key_contract_instance",
            ):
                raise ValueError(
                    f"Unexpected string '{json_value}' for SCVal, must be one of: void, ledger_key_contract_instance"
                )
            type = SCValType.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SCVal, got: {json_value}"
            )
        key = next(iter(json_value))
        type = SCValType.from_json_dict(key)
        if key == "bool":
            b = Boolean.from_json_dict(json_value["bool"])
            return cls(type=type, b=b)
        if key == "error":
            from .sc_error import SCError

            error = SCError.from_json_dict(json_value["error"])
            return cls(type=type, error=error)
        if key == "u32":
            from .uint32 import Uint32

            u32 = Uint32.from_json_dict(json_value["u32"])
            return cls(type=type, u32=u32)
        if key == "i32":
            from .int32 import Int32

            i32 = Int32.from_json_dict(json_value["i32"])
            return cls(type=type, i32=i32)
        if key == "u64":
            from .uint64 import Uint64

            u64 = Uint64.from_json_dict(json_value["u64"])
            return cls(type=type, u64=u64)
        if key == "i64":
            from .int64 import Int64

            i64 = Int64.from_json_dict(json_value["i64"])
            return cls(type=type, i64=i64)
        if key == "timepoint":
            from .time_point import TimePoint

            timepoint = TimePoint.from_json_dict(json_value["timepoint"])
            return cls(type=type, timepoint=timepoint)
        if key == "duration":
            from .duration import Duration

            duration = Duration.from_json_dict(json_value["duration"])
            return cls(type=type, duration=duration)
        if key == "u128":
            from .u_int128_parts import UInt128Parts

            u128 = UInt128Parts.from_json_dict(json_value["u128"])
            return cls(type=type, u128=u128)
        if key == "i128":
            from .int128_parts import Int128Parts

            i128 = Int128Parts.from_json_dict(json_value["i128"])
            return cls(type=type, i128=i128)
        if key == "u256":
            from .u_int256_parts import UInt256Parts

            u256 = UInt256Parts.from_json_dict(json_value["u256"])
            return cls(type=type, u256=u256)
        if key == "i256":
            from .int256_parts import Int256Parts

            i256 = Int256Parts.from_json_dict(json_value["i256"])
            return cls(type=type, i256=i256)
        if key == "bytes":
            from .sc_bytes import SCBytes

            bytes_val = SCBytes.from_json_dict(json_value["bytes"])
            return cls(type=type, bytes=bytes_val)
        if key == "string":
            from .sc_string import SCString

            str_val = SCString.from_json_dict(json_value["string"])
            return cls(type=type, str=str_val)
        if key == "symbol":
            from .sc_symbol import SCSymbol

            sym = SCSymbol.from_json_dict(json_value["symbol"])
            return cls(type=type, sym=sym)
        if key == "vec":
            from .sc_vec import SCVec

            vec = SCVec.from_json_dict(json_value["vec"])
            return cls(type=type, vec=vec)
        if key == "map":
            from .sc_map import SCMap

            map_val = SCMap.from_json_dict(json_value["map"])
            return cls(type=type, map=map_val)
        if key == "address":
            from .sc_address import SCAddress

            address = SCAddress.from_json_dict(json_value["address"])
            return cls(type=type, address=address)
        if key == "contract_instance":
            from .sc_contract_instance import SCContractInstance

            instance = SCContractInstance.from_json_dict(
                json_value["contract_instance"]
            )
            return cls(type=type, instance=instance)
        if key == "ledger_key_nonce":
            from .sc_nonce_key import SCNonceKey

            nonce_key = SCNonceKey.from_json_dict(json_value["ledger_key_nonce"])
            return cls(type=type, nonce_key=nonce_key)
        raise ValueError(f"Unknown key '{key}' for SCVal")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.b,
                self.error,
                self.u32,
                self.i32,
                self.u64,
                self.i64,
                self.timepoint,
                self.duration,
                self.u128,
                self.i128,
                self.u256,
                self.i256,
                self.bytes,
                self.str,
                self.sym,
                self.vec,
                self.map,
                self.address,
                self.instance,
                self.nonce_key,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.b == other.b
            and self.error == other.error
            and self.u32 == other.u32
            and self.i32 == other.i32
            and self.u64 == other.u64
            and self.i64 == other.i64
            and self.timepoint == other.timepoint
            and self.duration == other.duration
            and self.u128 == other.u128
            and self.i128 == other.i128
            and self.u256 == other.u256
            and self.i256 == other.i256
            and self.bytes == other.bytes
            and self.str == other.str
            and self.sym == other.sym
            and self.vec == other.vec
            and self.map == other.map
            and self.address == other.address
            and self.instance == other.instance
            and self.nonce_key == other.nonce_key
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.b is not None:
            out.append(f"b={self.b}")
        if self.error is not None:
            out.append(f"error={self.error}")
        if self.u32 is not None:
            out.append(f"u32={self.u32}")
        if self.i32 is not None:
            out.append(f"i32={self.i32}")
        if self.u64 is not None:
            out.append(f"u64={self.u64}")
        if self.i64 is not None:
            out.append(f"i64={self.i64}")
        if self.timepoint is not None:
            out.append(f"timepoint={self.timepoint}")
        if self.duration is not None:
            out.append(f"duration={self.duration}")
        if self.u128 is not None:
            out.append(f"u128={self.u128}")
        if self.i128 is not None:
            out.append(f"i128={self.i128}")
        if self.u256 is not None:
            out.append(f"u256={self.u256}")
        if self.i256 is not None:
            out.append(f"i256={self.i256}")
        if self.bytes is not None:
            out.append(f"bytes={self.bytes}")
        if self.str is not None:
            out.append(f"str={self.str}")
        if self.sym is not None:
            out.append(f"sym={self.sym}")
        if self.vec is not None:
            out.append(f"vec={self.vec}")
        if self.map is not None:
            out.append(f"map={self.map}")
        if self.address is not None:
            out.append(f"address={self.address}")
        if self.instance is not None:
            out.append(f"instance={self.instance}")
        if self.nonce_key is not None:
            out.append(f"nonce_key={self.nonce_key}")
        return f"<SCVal [{', '.join(out)}]>"
