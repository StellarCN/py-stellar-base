# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_spec_entry_kind import SCSpecEntryKind
from .sc_spec_function_v0 import SCSpecFunctionV0
from .sc_spec_udt_enum_v0 import SCSpecUDTEnumV0
from .sc_spec_udt_error_enum_v0 import SCSpecUDTErrorEnumV0
from .sc_spec_udt_struct_v0 import SCSpecUDTStructV0
from .sc_spec_udt_union_v0 import SCSpecUDTUnionV0

__all__ = ["SCSpecEntry"]


class SCSpecEntry:
    """
    XDR Source Code::

        union SCSpecEntry switch (SCSpecEntryKind kind)
        {
        case SC_SPEC_ENTRY_FUNCTION_V0:
            SCSpecFunctionV0 functionV0;
        case SC_SPEC_ENTRY_UDT_STRUCT_V0:
            SCSpecUDTStructV0 udtStructV0;
        case SC_SPEC_ENTRY_UDT_UNION_V0:
            SCSpecUDTUnionV0 udtUnionV0;
        case SC_SPEC_ENTRY_UDT_ENUM_V0:
            SCSpecUDTEnumV0 udtEnumV0;
        case SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0:
            SCSpecUDTErrorEnumV0 udtErrorEnumV0;
        };
    """

    def __init__(
        self,
        kind: SCSpecEntryKind,
        function_v0: SCSpecFunctionV0 = None,
        udt_struct_v0: SCSpecUDTStructV0 = None,
        udt_union_v0: SCSpecUDTUnionV0 = None,
        udt_enum_v0: SCSpecUDTEnumV0 = None,
        udt_error_enum_v0: SCSpecUDTErrorEnumV0 = None,
    ) -> None:
        self.kind = kind
        self.function_v0 = function_v0
        self.udt_struct_v0 = udt_struct_v0
        self.udt_union_v0 = udt_union_v0
        self.udt_enum_v0 = udt_enum_v0
        self.udt_error_enum_v0 = udt_error_enum_v0

    def pack(self, packer: Packer) -> None:
        self.kind.pack(packer)
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_FUNCTION_V0:
            if self.function_v0 is None:
                raise ValueError("function_v0 should not be None.")
            self.function_v0.pack(packer)
            return
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_STRUCT_V0:
            if self.udt_struct_v0 is None:
                raise ValueError("udt_struct_v0 should not be None.")
            self.udt_struct_v0.pack(packer)
            return
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_UNION_V0:
            if self.udt_union_v0 is None:
                raise ValueError("udt_union_v0 should not be None.")
            self.udt_union_v0.pack(packer)
            return
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ENUM_V0:
            if self.udt_enum_v0 is None:
                raise ValueError("udt_enum_v0 should not be None.")
            self.udt_enum_v0.pack(packer)
            return
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0:
            if self.udt_error_enum_v0 is None:
                raise ValueError("udt_error_enum_v0 should not be None.")
            self.udt_error_enum_v0.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecEntry:
        kind = SCSpecEntryKind.unpack(unpacker)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_FUNCTION_V0:
            function_v0 = SCSpecFunctionV0.unpack(unpacker)
            return cls(kind=kind, function_v0=function_v0)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_STRUCT_V0:
            udt_struct_v0 = SCSpecUDTStructV0.unpack(unpacker)
            return cls(kind=kind, udt_struct_v0=udt_struct_v0)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_UNION_V0:
            udt_union_v0 = SCSpecUDTUnionV0.unpack(unpacker)
            return cls(kind=kind, udt_union_v0=udt_union_v0)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ENUM_V0:
            udt_enum_v0 = SCSpecUDTEnumV0.unpack(unpacker)
            return cls(kind=kind, udt_enum_v0=udt_enum_v0)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0:
            udt_error_enum_v0 = SCSpecUDTErrorEnumV0.unpack(unpacker)
            return cls(kind=kind, udt_error_enum_v0=udt_error_enum_v0)
        return cls(kind=kind)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.kind,
                self.function_v0,
                self.udt_struct_v0,
                self.udt_union_v0,
                self.udt_enum_v0,
                self.udt_error_enum_v0,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.kind == other.kind
            and self.function_v0 == other.function_v0
            and self.udt_struct_v0 == other.udt_struct_v0
            and self.udt_union_v0 == other.udt_union_v0
            and self.udt_enum_v0 == other.udt_enum_v0
            and self.udt_error_enum_v0 == other.udt_error_enum_v0
        )

    def __repr__(self):
        out = []
        out.append(f"kind={self.kind}")
        (
            out.append(f"function_v0={self.function_v0}")
            if self.function_v0 is not None
            else None
        )
        (
            out.append(f"udt_struct_v0={self.udt_struct_v0}")
            if self.udt_struct_v0 is not None
            else None
        )
        (
            out.append(f"udt_union_v0={self.udt_union_v0}")
            if self.udt_union_v0 is not None
            else None
        )
        (
            out.append(f"udt_enum_v0={self.udt_enum_v0}")
            if self.udt_enum_v0 is not None
            else None
        )
        (
            out.append(f"udt_error_enum_v0={self.udt_error_enum_v0}")
            if self.udt_error_enum_v0 is not None
            else None
        )
        return f"<SCSpecEntry [{', '.join(out)}]>"
