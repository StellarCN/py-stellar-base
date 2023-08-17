from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["TimePoint"]


class TimePoint(BaseScValAlias):
    """Represents a Soroban TimePoint type.

    :param value: the UNIX timestamp (in seconds)
    """

    def __init__(self, value: int):
        self.value = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        tp = stellar_xdr.TimePoint(stellar_xdr.Uint64(self.value))
        return stellar_xdr.SCVal.from_scv_timepoint(tp)

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "TimePoint":
        if sc_val.type != stellar_xdr.SCValType.SCV_TIMEPOINT:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.timepoint is not None
        return cls(sc_val.timepoint.time_point.uint64)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<TimePoint [value={self.value}]>"
