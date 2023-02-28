from .base import BaseScValAlias
from ...xdr import SCVal, SCValType, SCObject, SCObjectType, Int128Parts, Uint64

__all__ = ["Int128"]


class Int128(BaseScValAlias):
    """Represents a Soroban Int128 type.

    :param value: The 128-bit integer value.
    """

    def __init__(self, value: int):
        if value < -(2 ** 127) or value > 2 ** 127 - 1:
            raise ValueError("Invalid Int128 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        v = self.value & (2 ** 128 - 1)
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_I128,
                i128=Int128Parts(
                    lo=Uint64(v & (2 ** 64 - 1)),
                    hi=Uint64(v >> 64),
                ),
            ),
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Int128":
        assert sc_val.obj is not None
        if (
                sc_val.type != SCValType.SCV_OBJECT
                or sc_val.obj.type != SCObjectType.SCO_I128
        ):
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj.i128 is not None
        v = sc_val.obj.i128.lo.uint64 + (sc_val.obj.i128.hi.uint64 << 64)
        if v >= 2 ** 127:
            v -= 2 ** 128
        return cls(v)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Int128 [value={self.value}]>"
