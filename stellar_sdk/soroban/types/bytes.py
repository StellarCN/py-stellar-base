from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["Bytes"]


class Bytes(BaseScValAlias):
    """Represents a Soroban Bytes type.

    :param value: The bytes value.
    """

    def __init__(self, value: bytes):
        self.value = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_bytes(stellar_xdr.SCBytes(self.value))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Bytes":
        if sc_val.type != stellar_xdr.SCValType.SCV_BYTES:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.bytes is not None
        return cls(sc_val.bytes.sc_bytes)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Bytes [value={self.value!r}]>"
