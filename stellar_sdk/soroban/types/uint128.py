from .base import BaseScValAlias
from ... import xdr as stellar_xdr

__all__ = ["Uint128"]


class Uint128(BaseScValAlias):
    """Represents a Soroban Uint128 type.

    :param value: The 128-bit unsigned integer value.
    """

    def __init__(self, value: int):
        if value < 0 or value > 2**128 - 1:
            raise ValueError("Invalid Uint128 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        u128 = stellar_xdr.Int128Parts(
            lo=stellar_xdr.Uint64(self.value & (2**64 - 1)),
            hi=stellar_xdr.Uint64(self.value >> 64),
        )
        return stellar_xdr.SCVal.from_scv_u128(u128)

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Uint128":
        if sc_val.type != stellar_xdr.SCValType.SCV_U128:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.u128 is not None
        return cls(sc_val.u128.lo.uint64 + (sc_val.u128.hi.uint64 << 64))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Uint128 [value={self.value}]>"
