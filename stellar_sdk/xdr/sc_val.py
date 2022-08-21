# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import Optional
from xdrlib import Packer, Unpacker

from .int32 import Int32
from .int64 import Int64
from .sc_object import SCObject
from .sc_static import SCStatic
from .sc_status import SCStatus
from .sc_symbol import SCSymbol
from .sc_val_type import SCValType
from .uint32 import Uint32
from .uint64 import Uint64

__all__ = ["SCVal"]


class SCVal:
    """
    XDR Source Code::

        union SCVal switch (SCValType type)
        {
        case SCV_U63:
            int64 u63;
        case SCV_U32:
            uint32 u32;
        case SCV_I32:
            int32 i32;
        case SCV_STATIC:
            SCStatic ic;
        case SCV_OBJECT:
            SCObject* obj;
        case SCV_SYMBOL:
            SCSymbol sym;
        case SCV_BITSET:
            uint64 bits;
        case SCV_STATUS:
            SCStatus status;
        };
    """

    def __init__(
        self,
        type: SCValType,
        u63: Int64 = None,
        u32: Uint32 = None,
        i32: Int32 = None,
        ic: SCStatic = None,
        obj: Optional[SCObject] = None,
        sym: SCSymbol = None,
        bits: Uint64 = None,
        status: SCStatus = None,
    ) -> None:
        self.type = type
        self.u63 = u63
        self.u32 = u32
        self.i32 = i32
        self.ic = ic
        self.obj = obj
        self.sym = sym
        self.bits = bits
        self.status = status

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCValType.SCV_U63:
            if self.u63 is None:
                raise ValueError("u63 should not be None.")
            self.u63.pack(packer)
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
        if self.type == SCValType.SCV_STATIC:
            if self.ic is None:
                raise ValueError("ic should not be None.")
            self.ic.pack(packer)
            return
        if self.type == SCValType.SCV_OBJECT:
            if self.obj is None:
                packer.pack_uint(0)
            else:
                packer.pack_uint(1)
                if self.obj is None:
                    raise ValueError("obj should not be None.")
                self.obj.pack(packer)
            return
        if self.type == SCValType.SCV_SYMBOL:
            if self.sym is None:
                raise ValueError("sym should not be None.")
            self.sym.pack(packer)
            return
        if self.type == SCValType.SCV_BITSET:
            if self.bits is None:
                raise ValueError("bits should not be None.")
            self.bits.pack(packer)
            return
        if self.type == SCValType.SCV_STATUS:
            if self.status is None:
                raise ValueError("status should not be None.")
            self.status.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCVal":
        type = SCValType.unpack(unpacker)
        if type == SCValType.SCV_U63:
            u63 = Int64.unpack(unpacker)
            return cls(type=type, u63=u63)
        if type == SCValType.SCV_U32:
            u32 = Uint32.unpack(unpacker)
            return cls(type=type, u32=u32)
        if type == SCValType.SCV_I32:
            i32 = Int32.unpack(unpacker)
            return cls(type=type, i32=i32)
        if type == SCValType.SCV_STATIC:
            ic = SCStatic.unpack(unpacker)
            return cls(type=type, ic=ic)
        if type == SCValType.SCV_OBJECT:
            obj = SCObject.unpack(unpacker) if unpacker.unpack_uint() else None
            return cls(type=type, obj=obj)
        if type == SCValType.SCV_SYMBOL:
            sym = SCSymbol.unpack(unpacker)
            return cls(type=type, sym=sym)
        if type == SCValType.SCV_BITSET:
            bits = Uint64.unpack(unpacker)
            return cls(type=type, bits=bits)
        if type == SCValType.SCV_STATUS:
            status = SCStatus.unpack(unpacker)
            return cls(type=type, status=status)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCVal":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCVal":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.u63 == other.u63
            and self.u32 == other.u32
            and self.i32 == other.i32
            and self.ic == other.ic
            and self.obj == other.obj
            and self.sym == other.sym
            and self.bits == other.bits
            and self.status == other.status
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"u63={self.u63}") if self.u63 is not None else None
        out.append(f"u32={self.u32}") if self.u32 is not None else None
        out.append(f"i32={self.i32}") if self.i32 is not None else None
        out.append(f"ic={self.ic}") if self.ic is not None else None
        out.append(f"obj={self.obj}") if self.obj is not None else None
        out.append(f"sym={self.sym}") if self.sym is not None else None
        out.append(f"bits={self.bits}") if self.bits is not None else None
        out.append(f"status={self.status}") if self.status is not None else None
        return f"<SCVal [{', '.join(out)}]>"
