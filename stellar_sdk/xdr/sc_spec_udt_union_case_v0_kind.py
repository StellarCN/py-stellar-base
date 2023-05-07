# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib3 import Packer, Unpacker

__all__ = ["SCSpecUDTUnionCaseV0Kind"]


class SCSpecUDTUnionCaseV0Kind(IntEnum):
    """
    XDR Source Code::

        enum SCSpecUDTUnionCaseV0Kind
        {
            SC_SPEC_UDT_UNION_CASE_VOID_V0 = 0,
            SC_SPEC_UDT_UNION_CASE_TUPLE_V0 = 1
        };
    """

    SC_SPEC_UDT_UNION_CASE_VOID_V0 = 0
    SC_SPEC_UDT_UNION_CASE_TUPLE_V0 = 1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCSpecUDTUnionCaseV0Kind":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCSpecUDTUnionCaseV0Kind":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCSpecUDTUnionCaseV0Kind":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
