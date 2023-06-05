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
        value_bytes = self.value.to_bytes(16, "big", signed=False)
        u128 = stellar_xdr.UInt128Parts(
            hi=stellar_xdr.Uint64(
                int.from_bytes(value_bytes[0:8], "big", signed=False)
            ),
            lo=stellar_xdr.Uint64(
                int.from_bytes(value_bytes[8:16], "big", signed=False)
            ),
        )
        return stellar_xdr.SCVal.from_scv_u128(u128)

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Uint128":
        if sc_val.type != stellar_xdr.SCValType.SCV_U128:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.u128 is not None
        value_bytes = sc_val.u128.hi.uint64.to_bytes(
            8, "big", signed=False
        ) + sc_val.u128.lo.uint64.to_bytes(8, "big", signed=False)
        v = int.from_bytes(value_bytes, "big", signed=False)
        return cls(v)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Uint128 [value={self.value}]>"
