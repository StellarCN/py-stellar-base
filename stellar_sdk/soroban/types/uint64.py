from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["Uint64"]


class Uint64(BaseScValAlias):
    """Represents a Soroban Uint64 type.

    :param value: The 64-bit unsigned integer value.
    """

    def __init__(self, value: int):
        if value < 0 or value > 2**64 - 1:
            raise ValueError("Invalid Uint64 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_u64(stellar_xdr.Uint64(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Uint64":
        if sc_val.type != stellar_xdr.SCValType.SCV_U64:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.u64 is not None
        return cls(sc_val.u64.uint64)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Uint64 [value={self.value}]>"
