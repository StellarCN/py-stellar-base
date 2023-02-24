from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, Uint32 as XdrUint32

__all__ = ["Uint32"]


class Uint32(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(SCValType.SCV_U32, u32=XdrUint32(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Uint32":
        if sc_val.type != SCValType.SCV_U32:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.u32 is not None
        return cls(sc_val.u32.uint32)
