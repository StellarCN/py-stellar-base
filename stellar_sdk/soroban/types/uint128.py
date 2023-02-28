from .base import BaseScValAlias
from ...xdr import SCVal, SCValType, SCObject, SCObjectType, Int128Parts, Uint64

__all__ = ["Uint128"]


class Uint128(BaseScValAlias):
    """Represents a Soroban Uint128 type.

    :param value: The 128-bit unsigned integer value.
    """

    def __init__(self, value: int):
        if value < 0 or value > 2 ** 128 - 1:
            raise ValueError("Invalid Uint128 value.")
        self.value: int = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_U128,
                u128=Int128Parts(
                    lo=Uint64(self.value & (2 ** 64 - 1)),
                    hi=Uint64(self.value >> 64),
                ),
            ),
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Uint128":
        assert sc_val.obj is not None
        if (
                sc_val.type != SCValType.SCV_OBJECT
                or sc_val.obj.type != SCObjectType.SCO_U128
        ):
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj.u128 is not None
        return cls(sc_val.obj.u128.lo.uint64 + (sc_val.obj.u128.hi.uint64 << 64))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Uint128 [value={self.value}]>"
