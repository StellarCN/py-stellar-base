# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_spec_udt_union_case_tuple_v0 import SCSpecUDTUnionCaseTupleV0
from .sc_spec_udt_union_case_v0_kind import SCSpecUDTUnionCaseV0Kind
from .sc_spec_udt_union_case_void_v0 import SCSpecUDTUnionCaseVoidV0

__all__ = ["SCSpecUDTUnionCaseV0"]


class SCSpecUDTUnionCaseV0:
    """
    XDR Source Code::

        union SCSpecUDTUnionCaseV0 switch (SCSpecUDTUnionCaseV0Kind kind)
        {
        case SC_SPEC_UDT_UNION_CASE_VOID_V0:
            SCSpecUDTUnionCaseVoidV0 voidCase;
        case SC_SPEC_UDT_UNION_CASE_TUPLE_V0:
            SCSpecUDTUnionCaseTupleV0 tupleCase;
        };
    """

    def __init__(
        self,
        kind: SCSpecUDTUnionCaseV0Kind,
        void_case: SCSpecUDTUnionCaseVoidV0 = None,
        tuple_case: SCSpecUDTUnionCaseTupleV0 = None,
    ) -> None:
        self.kind = kind
        self.void_case = void_case
        self.tuple_case = tuple_case

    def pack(self, packer: Packer) -> None:
        self.kind.pack(packer)
        if self.kind == SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_VOID_V0:
            if self.void_case is None:
                raise ValueError("void_case should not be None.")
            self.void_case.pack(packer)
            return
        if self.kind == SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_TUPLE_V0:
            if self.tuple_case is None:
                raise ValueError("tuple_case should not be None.")
            self.tuple_case.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecUDTUnionCaseV0:
        kind = SCSpecUDTUnionCaseV0Kind.unpack(unpacker)
        if kind == SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_VOID_V0:
            void_case = SCSpecUDTUnionCaseVoidV0.unpack(unpacker)
            return cls(kind=kind, void_case=void_case)
        if kind == SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_TUPLE_V0:
            tuple_case = SCSpecUDTUnionCaseTupleV0.unpack(unpacker)
            return cls(kind=kind, tuple_case=tuple_case)
        return cls(kind=kind)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecUDTUnionCaseV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecUDTUnionCaseV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.kind,
                self.void_case,
                self.tuple_case,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.kind == other.kind
            and self.void_case == other.void_case
            and self.tuple_case == other.tuple_case
        )

    def __repr__(self):
        out = []
        out.append(f"kind={self.kind}")
        (
            out.append(f"void_case={self.void_case}")
            if self.void_case is not None
            else None
        )
        (
            out.append(f"tuple_case={self.tuple_case}")
            if self.tuple_case is not None
            else None
        )
        return f"<SCSpecUDTUnionCaseV0 [{', '.join(out)}]>"
