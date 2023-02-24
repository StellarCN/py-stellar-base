from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, SCObject, SCObjectType, Int128Parts, Uint64

__all__ = ["Int128"]


class Int128(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        v = self.value & (2**128 - 1)
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_I128,
                i128=Int128Parts(
                    lo=Uint64(v & (2**64 - 1)),
                    hi=Uint64(v >> 64),
                ),
            ),
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Int128":
        assert sc_val.obj is not None
        if (
            sc_val.type != SCValType.SCV_OBJECT
            or sc_val.obj.type != SCObjectType.SCO_I128
        ):
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj.i128 is not None
        return cls(sc_val.obj.i128.lo.uint64 + (sc_val.obj.i128.hi.uint64 << 64))
