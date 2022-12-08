from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, SCObject, SCObjectType, Int128Parts, Uint64

__all__ = ["Int128"]


class Int128(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def _to_xdr_sc_val(self) -> SCVal:
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
