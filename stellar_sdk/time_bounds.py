from .exceptions import ValueError
from .xdr import xdr as stellarxdr

__all__ = ["TimeBounds"]


class TimeBounds:
    """TimeBounds represents the time interval that a transaction is valid.

    The UNIX timestamp (in seconds), determined by ledger time,
    of a lower and upper bound of when this transaction will be valid.
    If a transaction is submitted too early or too late,
    it will fail to make it into the transaction set.
    **max_time** equal 0 means that it’s not set.

    See `Stellar's documentation on Transactions
    <https://www.stellar.org/developers/guides/concepts/transactions.html#time-bounds>`__
    for more information on how TimeBounds are used within transactions.


    :param min_time: the UNIX timestamp (in seconds)
    :param max_time: the UNIX timestamp (in seconds)
    :raises: :exc:`ValueError <stellar_sdk.exceptions.ValueError>`: if ``max_time`` less than ``min_time``.
    """

    def __init__(self, min_time: int, max_time: int) -> None:
        if min_time < 0:
            raise ValueError("min_time cannot be negative.")

        if max_time < 0:
            raise ValueError("max_time cannot be negative.")

        if 0 < max_time < min_time:
            raise ValueError("max_time must be >= min_time.")

        self.min_time: int = min_time
        self.max_time: int = max_time

    def to_xdr_object(self) -> stellarxdr.TimeBounds:
        """Returns the xdr object for this TimeBounds object.

        :return: XDR TimeBounds object
        """
        min_time = stellarxdr.TimePoint(stellarxdr.Uint64(self.min_time))
        max_time = stellarxdr.TimePoint(stellarxdr.Uint64(self.max_time))
        return stellarxdr.TimeBounds(min_time, max_time)

    @classmethod
    def from_xdr_object(
        cls, time_bounds_xdr_object: stellarxdr.TimeBounds
    ) -> "TimeBounds":
        """Create a :class:`TimeBounds` from an XDR TimeBounds object.

        :param time_bounds_xdr_object: The XDR TimeBounds object.
        :return: A new :class:`TimeBounds` object from the given XDR TimeBounds object.
        """
        return cls(
            min_time=time_bounds_xdr_object.min_time.time_point.uint64,
            max_time=time_bounds_xdr_object.max_time.time_point.uint64,
        )

    def to_xdr(self) -> str:
        """Get the base64 encoded XDR string representing this
        :class:`TimeBounds`.

        :return: XDR :class:`TimeBounds` base64 string object
        """
        return self.to_xdr_object().to_xdr()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TimeBounds":
        """Create a new :class:`TimeBounds` from an XDR string.

        :param xdr: The XDR string that represents a :class:`TimeBounds`.

        :return: A new :class:`TimeBounds` object from the given XDR TimeBounds base64 string object.
        """
        xdr_obj = stellarxdr.TimeBounds.from_xdr(xdr)
        return cls.from_xdr_object(xdr_obj)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.min_time == other.min_time and self.max_time == other.max_time

    def __str__(self):
        return "<TimeBounds [min_time={min_time}, max_time={max_time}]>".format(
            min_time=self.min_time, max_time=self.max_time
        )
