from .base import BaseScValAlias
from ... import xdr as stellar_xdr

__all__ = ["Bool"]


class Bool(BaseScValAlias):
    """Represents a Soroban Bool type.

    :param value: The bool value.
    """

    def __init__(self, value: bool):
        self.value = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_bool(self.value)

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Bool":
        if sc_val.type != stellar_xdr.SCValType.SCV_BOOL:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.b is not None
        return cls(sc_val.b)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Bool [value={self.value}]>"
