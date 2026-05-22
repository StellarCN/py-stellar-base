# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_SC_SPEC_ENTRY_KIND_MAP = {
    0: "function_v0",
    1: "udt_struct_v0",
    2: "udt_union_v0",
    3: "udt_enum_v0",
    4: "udt_error_enum_v0",
    5: "event_v0",
}
_SC_SPEC_ENTRY_KIND_REVERSE_MAP = {
    "function_v0": 0,
    "udt_struct_v0": 1,
    "udt_union_v0": 2,
    "udt_enum_v0": 3,
    "udt_error_enum_v0": 4,
    "event_v0": 5,
}
__all__ = ["SCSpecEntryKind"]


class SCSpecEntryKind(IntEnum):
    """
    XDR Source Code::

        enum SCSpecEntryKind
        {
            SC_SPEC_ENTRY_FUNCTION_V0 = 0,
            SC_SPEC_ENTRY_UDT_STRUCT_V0 = 1,
            SC_SPEC_ENTRY_UDT_UNION_V0 = 2,
            SC_SPEC_ENTRY_UDT_ENUM_V0 = 3,
            SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0 = 4,
            SC_SPEC_ENTRY_EVENT_V0 = 5
        };
    """

    SC_SPEC_ENTRY_FUNCTION_V0 = 0
    SC_SPEC_ENTRY_UDT_STRUCT_V0 = 1
    SC_SPEC_ENTRY_UDT_UNION_V0 = 2
    SC_SPEC_ENTRY_UDT_ENUM_V0 = 3
    SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0 = 4
    SC_SPEC_ENTRY_EVENT_V0 = 5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecEntryKind:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecEntryKind:
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
    def from_xdr(cls, xdr: str) -> SCSpecEntryKind:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecEntryKind:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _SC_SPEC_ENTRY_KIND_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> SCSpecEntryKind:
        return cls(_SC_SPEC_ENTRY_KIND_REVERSE_MAP[json_value])
