from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, Int32 as XdrInt32

__all__ = ["Int32"]


class Int32(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(SCValType.SCV_I32, i32=XdrInt32(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Int32":
        if sc_val.type != SCValType.SCV_I32:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.i32 is not None
        return cls(sc_val.i32.int32)
