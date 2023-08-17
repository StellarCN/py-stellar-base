from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["Duration"]


class Duration(BaseScValAlias):
    """Represents a Soroban Duration type.

    :param value: The duration value in seconds.
    """

    def __init__(self, value: int):
        self.value = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        tp = stellar_xdr.Duration(stellar_xdr.Uint64(self.value))
        return stellar_xdr.SCVal.from_scv_duration(tp)

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Duration":
        if sc_val.type != stellar_xdr.SCValType.SCV_DURATION:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.timepoint is not None
        return cls(sc_val.timepoint.time_point.uint64)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Duration [value={self.value}]>"
