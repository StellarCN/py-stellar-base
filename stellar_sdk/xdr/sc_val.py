# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Optional

from xdrlib3 import Packer, Unpacker

from .base import Boolean
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
        case SCV_LEDGER_KEY_CONTRACT_INSTANCE:
            void;
        case SCV_LEDGER_KEY_NONCE:
            SCNonceKey nonce_key;

        case SCV_CONTRACT_INSTANCE:
            SCContractInstance instance;
        };
    """

    def __init__(
        self,
        type: SCValType,
        b: bool = None,
        error: SCError = None,
        u32: Uint32 = None,
        i32: Int32 = None,
        u64: Uint64 = None,
        i64: Int64 = None,
        timepoint: TimePoint = None,
        duration: Duration = None,
        u128: UInt128Parts = None,
        i128: Int128Parts = None,
        u256: UInt256Parts = None,
        i256: Int256Parts = None,
        bytes: SCBytes = None,
        str: SCString = None,
        sym: SCSymbol = None,
        vec: Optional[SCVec] = None,
        map: Optional[SCMap] = None,
        address: SCAddress = None,
        nonce_key: SCNonceKey = None,
        instance: SCContractInstance = None,
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
        self.nonce_key = nonce_key
        self.instance = instance

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
        if self.type == SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE:
            return
        if self.type == SCValType.SCV_LEDGER_KEY_NONCE:
            if self.nonce_key is None:
                raise ValueError("nonce_key should not be None.")
            self.nonce_key.pack(packer)
            return
        if self.type == SCValType.SCV_CONTRACT_INSTANCE:
            if self.instance is None:
                raise ValueError("instance should not be None.")
            self.instance.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCVal:
        type = SCValType.unpack(unpacker)
        if type == SCValType.SCV_BOOL:
            b = Boolean.unpack(unpacker)
            return cls(type=type, b=b)
        if type == SCValType.SCV_VOID:
            return cls(type=type)
        if type == SCValType.SCV_ERROR:
            from .sc_error import SCError

            error = SCError.unpack(unpacker)
            return cls(type=type, error=error)
        if type == SCValType.SCV_U32:
            from .uint32 import Uint32

            u32 = Uint32.unpack(unpacker)
            return cls(type=type, u32=u32)
        if type == SCValType.SCV_I32:
            from .int32 import Int32

            i32 = Int32.unpack(unpacker)
            return cls(type=type, i32=i32)
        if type == SCValType.SCV_U64:
            from .uint64 import Uint64

            u64 = Uint64.unpack(unpacker)
            return cls(type=type, u64=u64)
        if type == SCValType.SCV_I64:
            from .int64 import Int64

            i64 = Int64.unpack(unpacker)
            return cls(type=type, i64=i64)
        if type == SCValType.SCV_TIMEPOINT:
            from .time_point import TimePoint

            timepoint = TimePoint.unpack(unpacker)
            return cls(type=type, timepoint=timepoint)
        if type == SCValType.SCV_DURATION:
            from .duration import Duration

            duration = Duration.unpack(unpacker)
            return cls(type=type, duration=duration)
        if type == SCValType.SCV_U128:
            from .u_int128_parts import UInt128Parts

            u128 = UInt128Parts.unpack(unpacker)
            return cls(type=type, u128=u128)
        if type == SCValType.SCV_I128:
            from .int128_parts import Int128Parts

            i128 = Int128Parts.unpack(unpacker)
            return cls(type=type, i128=i128)
        if type == SCValType.SCV_U256:
            from .u_int256_parts import UInt256Parts

            u256 = UInt256Parts.unpack(unpacker)
            return cls(type=type, u256=u256)
        if type == SCValType.SCV_I256:
            from .int256_parts import Int256Parts

            i256 = Int256Parts.unpack(unpacker)
            return cls(type=type, i256=i256)
        if type == SCValType.SCV_BYTES:
            from .sc_bytes import SCBytes

            bytes = SCBytes.unpack(unpacker)
            return cls(type=type, bytes=bytes)
        if type == SCValType.SCV_STRING:
            from .sc_string import SCString

            str = SCString.unpack(unpacker)
            return cls(type=type, str=str)
        if type == SCValType.SCV_SYMBOL:
            from .sc_symbol import SCSymbol

            sym = SCSymbol.unpack(unpacker)
            return cls(type=type, sym=sym)
        if type == SCValType.SCV_VEC:
            from .sc_vec import SCVec

            vec = SCVec.unpack(unpacker) if unpacker.unpack_uint() else None
            return cls(type=type, vec=vec)
        if type == SCValType.SCV_MAP:
            from .sc_map import SCMap

            map = SCMap.unpack(unpacker) if unpacker.unpack_uint() else None
            return cls(type=type, map=map)
        if type == SCValType.SCV_ADDRESS:
            from .sc_address import SCAddress

            address = SCAddress.unpack(unpacker)
            return cls(type=type, address=address)
        if type == SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE:
            return cls(type=type)
        if type == SCValType.SCV_LEDGER_KEY_NONCE:
            from .sc_nonce_key import SCNonceKey

            nonce_key = SCNonceKey.unpack(unpacker)
            return cls(type=type, nonce_key=nonce_key)
        if type == SCValType.SCV_CONTRACT_INSTANCE:
            from .sc_contract_instance import SCContractInstance

            instance = SCContractInstance.unpack(unpacker)
            return cls(type=type, instance=instance)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCVal:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCVal:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
                self.nonce_key,
                self.instance,
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
            and self.nonce_key == other.nonce_key
            and self.instance == other.instance
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"b={self.b}") if self.b is not None else None
        out.append(f"error={self.error}") if self.error is not None else None
        out.append(f"u32={self.u32}") if self.u32 is not None else None
        out.append(f"i32={self.i32}") if self.i32 is not None else None
        out.append(f"u64={self.u64}") if self.u64 is not None else None
        out.append(f"i64={self.i64}") if self.i64 is not None else None
        (
            out.append(f"timepoint={self.timepoint}")
            if self.timepoint is not None
            else None
        )
        out.append(f"duration={self.duration}") if self.duration is not None else None
        out.append(f"u128={self.u128}") if self.u128 is not None else None
        out.append(f"i128={self.i128}") if self.i128 is not None else None
        out.append(f"u256={self.u256}") if self.u256 is not None else None
        out.append(f"i256={self.i256}") if self.i256 is not None else None
        out.append(f"bytes={self.bytes}") if self.bytes is not None else None
        out.append(f"str={self.str}") if self.str is not None else None
        out.append(f"sym={self.sym}") if self.sym is not None else None
        out.append(f"vec={self.vec}") if self.vec is not None else None
        out.append(f"map={self.map}") if self.map is not None else None
        out.append(f"address={self.address}") if self.address is not None else None
        (
            out.append(f"nonce_key={self.nonce_key}")
            if self.nonce_key is not None
            else None
        )
        out.append(f"instance={self.instance}") if self.instance is not None else None
        return f"<SCVal [{', '.join(out)}]>"
