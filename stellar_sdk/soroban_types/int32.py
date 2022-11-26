from ..xdr import SCVal, SCValType, Int32 as XdrInt32

from .base import BaseScValAlias

__all__ = ["Int32"]


class Int32(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal(SCValType.SCV_I32, i32=XdrInt32(self.value))
