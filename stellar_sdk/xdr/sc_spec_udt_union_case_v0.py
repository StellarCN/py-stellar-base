# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
        void_case: Optional[SCSpecUDTUnionCaseVoidV0] = None,
        tuple_case: Optional[SCSpecUDTUnionCaseTupleV0] = None,
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
        raise ValueError("Invalid kind.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCSpecUDTUnionCaseV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        kind = SCSpecUDTUnionCaseV0Kind.unpack(unpacker)
        if kind == SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_VOID_V0:
            void_case = SCSpecUDTUnionCaseVoidV0.unpack(unpacker, depth_limit - 1)
            return cls(kind=kind, void_case=void_case)
        if kind == SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_TUPLE_V0:
            tuple_case = SCSpecUDTUnionCaseTupleV0.unpack(unpacker, depth_limit - 1)
            return cls(kind=kind, tuple_case=tuple_case)
        raise ValueError("Invalid kind.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecUDTUnionCaseV0:
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
    def from_xdr(cls, xdr: str) -> SCSpecUDTUnionCaseV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCSpecUDTUnionCaseV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.kind == SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_VOID_V0:
            assert self.void_case is not None
            return {"void_v0": self.void_case.to_json_dict()}
        if self.kind == SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_TUPLE_V0:
            assert self.tuple_case is not None
            return {"tuple_v0": self.tuple_case.to_json_dict()}
        raise ValueError(f"Unknown kind in SCSpecUDTUnionCaseV0: {self.kind}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> SCSpecUDTUnionCaseV0:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SCSpecUDTUnionCaseV0, got: {json_value}"
            )
        key = next(iter(json_value))
        kind = SCSpecUDTUnionCaseV0Kind.from_json_dict(key)
        if key == "void_v0":
            void_case = SCSpecUDTUnionCaseVoidV0.from_json_dict(json_value["void_v0"])
            return cls(kind=kind, void_case=void_case)
        if key == "tuple_v0":
            tuple_case = SCSpecUDTUnionCaseTupleV0.from_json_dict(
                json_value["tuple_v0"]
            )
            return cls(kind=kind, tuple_case=tuple_case)
        raise ValueError(f"Unknown key '{key}' for SCSpecUDTUnionCaseV0")

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
        if self.void_case is not None:
            out.append(f"void_case={self.void_case}")
        if self.tuple_case is not None:
            out.append(f"tuple_case={self.tuple_case}")
        return f"<SCSpecUDTUnionCaseV0 [{', '.join(out)}]>"
