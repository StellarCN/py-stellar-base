from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, SCObject, SCObjectType, Int64 as XdrInt64

__all__ = ["Int64"]


class Int64(BaseScValAlias):
    def __init__(self, value: int):
        if value < -(2**63) or value > 2**63 - 1:
            raise ValueError("Invalid Int64 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_I64,
                i64=XdrInt64(self.value),
            ),
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Int64":
        assert sc_val.obj is not None
        if (
            sc_val.type != SCValType.SCV_OBJECT
            or sc_val.obj.type != SCObjectType.SCO_I64
        ):
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj.i64 is not None
        return cls(sc_val.obj.i64.int64)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Int64 [value={self.value}]>"
