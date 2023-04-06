from .base import BaseScValAlias
from ... import xdr as stellar_xdr

__all__ = ["String"]


class String(BaseScValAlias):
    """Represents a Soroban String type.

    :param value: The string value.
    """

    # TODO: str?
    def __init__(self, value: bytes):
        self.value = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_string(str=stellar_xdr.SCString(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "String":
        if sc_val.type != stellar_xdr.SCValType.SCV_STRING:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.str is not None
        return cls(sc_val.str.sc_string)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<String [value={self.value!r}]>"
