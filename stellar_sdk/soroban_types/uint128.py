from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, SCObject, SCObjectType, Int128Parts, Uint64

__all__ = ["Uint128"]


class Uint128(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_U128,
                i128=Int128Parts(
                    lo=Uint64(self.value & (2**64 - 1)),
                    hi=Uint64(self.value >> 64),
                ),
            ),
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Uint128":
        assert sc_val.obj is not None
        if (
            sc_val.type != SCValType.SCV_OBJECT
            or sc_val.obj.type != SCObjectType.SCO_U128
        ):
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj.u128 is not None
        return cls(sc_val.obj.u128.lo.uint64 + (sc_val.obj.u128.hi.uint64 << 64))
