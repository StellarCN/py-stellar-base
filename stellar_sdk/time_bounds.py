import typing

from .stellarxdr import Xdr


class TimeBounds:
    def __init__(self, min_time: int, max_time: int) -> None:
        if 0 < max_time <= min_time:
            raise ValueError("max_time must be >= min_time.")

        self.min_time = min_time
        self.max_time = max_time

    def to_xdr_object(self) -> Xdr.types.TimeBounds:
        return Xdr.types.TimeBounds(self.min_time, self.max_time)

    @classmethod
    def from_xdr_object(cls, time_bounds: Xdr.types.TimeBounds) -> typing.Optional['TimeBounds']:
        return cls(time_bounds.minTime, time_bounds.maxTime)

    def __eq__(self, other: 'TimeBounds') -> bool:
        return self.min_time == other.min_time and self.max_time == other.max_time
