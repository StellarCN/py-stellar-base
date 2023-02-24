from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, Int64 as Int64

__all__ = ["Uint63"]


class Uint63(BaseScValAlias):
    def __init__(self, value: int):
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(SCValType.SCV_U63, u63=Int64(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Uint63":
        if sc_val.type != SCValType.SCV_U63:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.u63 is not None
        return cls(sc_val.u63.int64)
