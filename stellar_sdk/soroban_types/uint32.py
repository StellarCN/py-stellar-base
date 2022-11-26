from ..xdr import SCVal, SCValType, Uint32 as XdrUint32

from .base import BaseScValAlias

__all__ = ["Uint32"]


class Uint32(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal(SCValType.SCV_U32, u32=XdrUint32(self.value))
