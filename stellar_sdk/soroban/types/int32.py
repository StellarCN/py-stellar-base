from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["Int32"]


class Int32(BaseScValAlias):
    """Represents a Soroban Int32 type.

    :param value: The 32-bit integer value.
    """

    def __init__(self, value: int):
        if value < -(2**31) or value > 2**31 - 1:
            raise ValueError("Invalid Int32 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_i32(stellar_xdr.Int32(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Int32":
        if sc_val.type != stellar_xdr.SCValType.SCV_I32:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.i32 is not None
        return cls(sc_val.i32.int32)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Int32 [value={self.value}]>"
