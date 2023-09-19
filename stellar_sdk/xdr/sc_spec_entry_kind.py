# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

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
            SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0 = 4
        };
    """

    SC_SPEC_ENTRY_FUNCTION_V0 = 0
    SC_SPEC_ENTRY_UDT_STRUCT_V0 = 1
    SC_SPEC_ENTRY_UDT_UNION_V0 = 2
    SC_SPEC_ENTRY_UDT_ENUM_V0 = 3
    SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0 = 4

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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecEntryKind:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
