from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["Int128"]


class Int128(BaseScValAlias):
    """Represents a Soroban Int128 type.

    :param value: The 128-bit integer value.
    """

    def __init__(self, value: int):
        if value < -(2**127) or value > 2**127 - 1:
            raise ValueError("Invalid Int128 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        value_bytes = self.value.to_bytes(16, "big", signed=True)
        i128 = stellar_xdr.Int128Parts(
            hi=stellar_xdr.Int64(int.from_bytes(value_bytes[0:8], "big", signed=True)),
            lo=stellar_xdr.Uint64(
                int.from_bytes(value_bytes[8:16], "big", signed=False)
            ),
        )
        return stellar_xdr.SCVal.from_scv_i128(i128)

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Int128":
        if sc_val.type != stellar_xdr.SCValType.SCV_I128:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.i128 is not None
        value_bytes = sc_val.i128.hi.int64.to_bytes(
            8, "big", signed=True
        ) + sc_val.i128.lo.uint64.to_bytes(8, "big", signed=False)
        v = int.from_bytes(value_bytes, "big", signed=True)
        return cls(v)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Int128 [value={self.value}]>"
