from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["Int64"]


class Int64(BaseScValAlias):
    """Represents a Soroban Int64 type.

    :param value: The 64-bit integer value.
    """

    def __init__(self, value: int):
        if value < -(2**63) or value > 2**63 - 1:
            raise ValueError("Invalid Int64 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_i64(stellar_xdr.Int64(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Int64":
        if sc_val.type != stellar_xdr.SCValType.SCV_I64:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.i64 is not None
        return cls(sc_val.i64.int64)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Int64 [value={self.value}]>"
