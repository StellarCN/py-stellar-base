from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["Int256"]


class Int256(BaseScValAlias):
    """Represents a Soroban Int256 type.

    :param value: The 256-bit signed integer value.
    """

    def __init__(self, value: int):
        if value < -(2**255) or value > 2**255 - 1:
            raise ValueError("Invalid Int256 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        value_bytes = self.value.to_bytes(32, "big", signed=True)
        hi_hi, hi_lo, lo_hi, lo_lo = (
            int.from_bytes(value_bytes[0:8], "big", signed=True),
            int.from_bytes(value_bytes[8:16], "big", signed=False),
            int.from_bytes(value_bytes[16:24], "big", signed=False),
            int.from_bytes(value_bytes[24:32], "big", signed=False),
        )
        i256 = stellar_xdr.Int256Parts(
            hi_hi=stellar_xdr.Int64(hi_hi),
            hi_lo=stellar_xdr.Uint64(hi_lo),
            lo_hi=stellar_xdr.Uint64(lo_hi),
            lo_lo=stellar_xdr.Uint64(lo_lo),
        )
        return stellar_xdr.SCVal.from_scv_i256(i256)

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Int256":
        if sc_val.type != stellar_xdr.SCValType.SCV_I256:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.i256 is not None

        value_bytes = (
            sc_val.i256.hi_hi.int64.to_bytes(8, "big", signed=True)
            + sc_val.i256.hi_lo.uint64.to_bytes(8, "big", signed=False)
            + sc_val.i256.lo_hi.uint64.to_bytes(8, "big", signed=False)
            + sc_val.i256.lo_lo.uint64.to_bytes(8, "big", signed=False)
        )
        v = int.from_bytes(value_bytes, "big", signed=True)
        return cls(v)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Int256 [value={self.value}]>"
