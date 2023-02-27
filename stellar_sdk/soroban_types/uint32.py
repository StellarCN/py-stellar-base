from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, Uint32 as XdrUint32

__all__ = ["Uint32"]


class Uint32(BaseScValAlias):
    """Represents a Soroban Uint32 type.

    :param value: The 32-bit unsigned integer value.
    """

    def __init__(self, value: int):
        if value < 0 or value > 2**32 - 1:
            raise ValueError("Invalid Uint32 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(SCValType.SCV_U32, u32=XdrUint32(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Uint32":
        if sc_val.type != SCValType.SCV_U32:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.u32 is not None
        return cls(sc_val.u32.uint32)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Uint32 [value={self.value}]>"
