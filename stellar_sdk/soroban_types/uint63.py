from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, Int64 as Int64

__all__ = ["Uint63"]


class Uint63(BaseScValAlias):
    def __init__(self, value: int):
        if value < 0 or value > 2**63 - 1:
            raise ValueError("Invalid Uint63 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(SCValType.SCV_U63, u63=Int64(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Uint63":
        if sc_val.type != SCValType.SCV_U63:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.u63 is not None
        return cls(sc_val.u63.int64)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Uint63 [value={self.value}]>"
