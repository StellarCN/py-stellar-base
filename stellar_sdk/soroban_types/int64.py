from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, SCObject, SCObjectType, Int64 as XdrInt64

__all__ = ["Int64"]


class Int64(BaseScValAlias):
    def __init__(self, value: int):
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
