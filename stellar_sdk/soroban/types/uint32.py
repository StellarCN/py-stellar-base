from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["Uint32"]


class Uint32(BaseScValAlias):
    """Represents a Soroban Uint32 type.

    :param value: The 32-bit unsigned integer value.
    """

    def __init__(self, value: int):
        if value < 0 or value > 2**32 - 1:
            raise ValueError("Invalid Uint32 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_u32(u32=stellar_xdr.Uint32(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Uint32":
        if sc_val.type != stellar_xdr.SCValType.SCV_U32:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.u32 is not None
        return cls(sc_val.u32.uint32)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Uint32 [value={self.value}]>"
