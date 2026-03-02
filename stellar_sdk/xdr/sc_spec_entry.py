# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sc_spec_entry_kind import SCSpecEntryKind
from .sc_spec_event_v0 import SCSpecEventV0
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
        case SC_SPEC_ENTRY_EVENT_V0:
            SCSpecEventV0 eventV0;
        };
    """

    def __init__(
        self,
        kind: SCSpecEntryKind,
        function_v0: Optional[SCSpecFunctionV0] = None,
        udt_struct_v0: Optional[SCSpecUDTStructV0] = None,
        udt_union_v0: Optional[SCSpecUDTUnionV0] = None,
        udt_enum_v0: Optional[SCSpecUDTEnumV0] = None,
        udt_error_enum_v0: Optional[SCSpecUDTErrorEnumV0] = None,
        event_v0: Optional[SCSpecEventV0] = None,
    ) -> None:
        self.kind = kind
        self.function_v0 = function_v0
        self.udt_struct_v0 = udt_struct_v0
        self.udt_union_v0 = udt_union_v0
        self.udt_enum_v0 = udt_enum_v0
        self.udt_error_enum_v0 = udt_error_enum_v0
        self.event_v0 = event_v0

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
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_EVENT_V0:
            if self.event_v0 is None:
                raise ValueError("event_v0 should not be None.")
            self.event_v0.pack(packer)
            return
        raise ValueError("Invalid kind.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        kind = SCSpecEntryKind.unpack(unpacker)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_FUNCTION_V0:
            function_v0 = SCSpecFunctionV0.unpack(unpacker, depth_limit - 1)
            return cls(kind=kind, function_v0=function_v0)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_STRUCT_V0:
            udt_struct_v0 = SCSpecUDTStructV0.unpack(unpacker, depth_limit - 1)
            return cls(kind=kind, udt_struct_v0=udt_struct_v0)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_UNION_V0:
            udt_union_v0 = SCSpecUDTUnionV0.unpack(unpacker, depth_limit - 1)
            return cls(kind=kind, udt_union_v0=udt_union_v0)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ENUM_V0:
            udt_enum_v0 = SCSpecUDTEnumV0.unpack(unpacker, depth_limit - 1)
            return cls(kind=kind, udt_enum_v0=udt_enum_v0)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0:
            udt_error_enum_v0 = SCSpecUDTErrorEnumV0.unpack(unpacker, depth_limit - 1)
            return cls(kind=kind, udt_error_enum_v0=udt_error_enum_v0)
        if kind == SCSpecEntryKind.SC_SPEC_ENTRY_EVENT_V0:
            event_v0 = SCSpecEventV0.unpack(unpacker, depth_limit - 1)
            return cls(kind=kind, event_v0=event_v0)
        raise ValueError("Invalid kind.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecEntry:
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
    def from_xdr(cls, xdr: str) -> SCSpecEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_FUNCTION_V0:
            assert self.function_v0 is not None
            return {"function_v0": self.function_v0.to_json_dict()}
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_STRUCT_V0:
            assert self.udt_struct_v0 is not None
            return {"udt_struct_v0": self.udt_struct_v0.to_json_dict()}
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_UNION_V0:
            assert self.udt_union_v0 is not None
            return {"udt_union_v0": self.udt_union_v0.to_json_dict()}
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ENUM_V0:
            assert self.udt_enum_v0 is not None
            return {"udt_enum_v0": self.udt_enum_v0.to_json_dict()}
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0:
            assert self.udt_error_enum_v0 is not None
            return {"udt_error_enum_v0": self.udt_error_enum_v0.to_json_dict()}
        if self.kind == SCSpecEntryKind.SC_SPEC_ENTRY_EVENT_V0:
            assert self.event_v0 is not None
            return {"event_v0": self.event_v0.to_json_dict()}
        raise ValueError(f"Unknown kind in SCSpecEntry: {self.kind}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> SCSpecEntry:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SCSpecEntry, got: {json_value}"
            )
        key = next(iter(json_value))
        kind = SCSpecEntryKind.from_json_dict(key)
        if key == "function_v0":
            function_v0 = SCSpecFunctionV0.from_json_dict(json_value["function_v0"])
            return cls(kind=kind, function_v0=function_v0)
        if key == "udt_struct_v0":
            udt_struct_v0 = SCSpecUDTStructV0.from_json_dict(
                json_value["udt_struct_v0"]
            )
            return cls(kind=kind, udt_struct_v0=udt_struct_v0)
        if key == "udt_union_v0":
            udt_union_v0 = SCSpecUDTUnionV0.from_json_dict(json_value["udt_union_v0"])
            return cls(kind=kind, udt_union_v0=udt_union_v0)
        if key == "udt_enum_v0":
            udt_enum_v0 = SCSpecUDTEnumV0.from_json_dict(json_value["udt_enum_v0"])
            return cls(kind=kind, udt_enum_v0=udt_enum_v0)
        if key == "udt_error_enum_v0":
            udt_error_enum_v0 = SCSpecUDTErrorEnumV0.from_json_dict(
                json_value["udt_error_enum_v0"]
            )
            return cls(kind=kind, udt_error_enum_v0=udt_error_enum_v0)
        if key == "event_v0":
            event_v0 = SCSpecEventV0.from_json_dict(json_value["event_v0"])
            return cls(kind=kind, event_v0=event_v0)
        raise ValueError(f"Unknown key '{key}' for SCSpecEntry")

    def __hash__(self):
        return hash(
            (
                self.kind,
                self.function_v0,
                self.udt_struct_v0,
                self.udt_union_v0,
                self.udt_enum_v0,
                self.udt_error_enum_v0,
                self.event_v0,
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
            and self.event_v0 == other.event_v0
        )

    def __repr__(self):
        out = []
        out.append(f"kind={self.kind}")
        if self.function_v0 is not None:
            out.append(f"function_v0={self.function_v0}")
        if self.udt_struct_v0 is not None:
            out.append(f"udt_struct_v0={self.udt_struct_v0}")
        if self.udt_union_v0 is not None:
            out.append(f"udt_union_v0={self.udt_union_v0}")
        if self.udt_enum_v0 is not None:
            out.append(f"udt_enum_v0={self.udt_enum_v0}")
        if self.udt_error_enum_v0 is not None:
            out.append(f"udt_error_enum_v0={self.udt_error_enum_v0}")
        if self.event_v0 is not None:
            out.append(f"event_v0={self.event_v0}")
        return f"<SCSpecEntry [{', '.join(out)}]>"
