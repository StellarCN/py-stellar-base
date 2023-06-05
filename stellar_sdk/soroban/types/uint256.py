from .base import BaseScValAlias
from ... import xdr as stellar_xdr

__all__ = ["Uint256"]


class Uint256(BaseScValAlias):
    """Represents a Soroban Uint256 type.

    :param value: The 256-bit unsigned integer value.
    """

    def __init__(self, value: int):
        if value < 0 or value > 2**256 - 1:
            raise ValueError("Invalid Uint256 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        value_bytes = self.value.to_bytes(32, "big", signed=False)
        hi_hi, hi_lo, lo_hi, lo_lo = (
            int.from_bytes(value_bytes[0:8], "big", signed=False),
            int.from_bytes(value_bytes[8:16], "big", signed=False),
            int.from_bytes(value_bytes[16:24], "big", signed=False),
            int.from_bytes(value_bytes[24:32], "big", signed=False),
        )
        u256 = stellar_xdr.UInt256Parts(
            hi_hi=stellar_xdr.Uint64(hi_hi),
            hi_lo=stellar_xdr.Uint64(hi_lo),
            lo_hi=stellar_xdr.Uint64(lo_hi),
            lo_lo=stellar_xdr.Uint64(lo_lo),
        )
        return stellar_xdr.SCVal.from_scv_u256(u256)

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Uint256":
        if sc_val.type != stellar_xdr.SCValType.SCV_U256:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.u256 is not None
        value_bytes = (
            sc_val.u256.hi_hi.uint64.to_bytes(8, "big", signed=False)
            + sc_val.u256.hi_lo.uint64.to_bytes(8, "big", signed=False)
            + sc_val.u256.lo_hi.uint64.to_bytes(8, "big", signed=False)
            + sc_val.u256.lo_lo.uint64.to_bytes(8, "big", signed=False)
        )
        v = int.from_bytes(value_bytes, "big", signed=True)
        return cls(v)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Uint256 [value={self.value}]>"
