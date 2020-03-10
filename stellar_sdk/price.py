from .utils import best_rational_approximation
from .xdr import xdr as stellarxdr

__all__ = ["Price"]


class Price:
    """Create a new price. Price in Stellar is represented as a fraction.

      :param n: numerator
      :param d: denominator
    """

    def __init__(self, n: int, d: int) -> None:
        self.n: int = n
        self.d: int = d

    @classmethod
    def from_raw_price(cls, price: str) -> "Price":
        """Create a :class:`Price` from the given str price.

        :param price: the str price. (ex. `'0.125'`)
        :return: A new :class:`Price` object from the given str price.
        :raises: :exc:`NoApproximationError <stellar_sdk.exceptions.NoApproximationError>`:
            if the approximation could not not be found.
        """
        best_r = best_rational_approximation(price)
        n = best_r["n"]
        d = best_r["d"]
        return cls(n, d)

    def to_xdr_object(self) -> stellarxdr.Price:
        """Returns the xdr object for this price object.

        :return: XDR Price object
        """
        return stellarxdr.Price(n=stellarxdr.Int32(self.n), d=stellarxdr.Int32(self.d))

    @classmethod
    def from_xdr_object(cls, price_xdr_object: stellarxdr.Price) -> "Price":
        """Create a :class:`Price` from an XDR Asset object.

        :param price_xdr_object: The XDR Price object.
        :return: A new :class:`Price` object from the given XDR Price object.
        """
        n = price_xdr_object.n.int32
        d = price_xdr_object.d.int32
        return cls(n, d)

    def to_xdr(self) -> str:
        """Get the base64 encoded XDR string representing this
        :class:`Price`.

        :return: XDR :class:`Price` base64 string object
        """
        return self.to_xdr_object().to_xdr()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Price":
        """Create a new :class:`Price` from an XDR string.

        :param xdr: The XDR string that represents a :class:`Price`.

        :return: A new :class:`Price` object from the given XDR Price base64 string object.
        """
        xdr_obj = stellarxdr.Price.from_xdr(xdr)
        return cls.from_xdr_object(xdr_obj)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.n == other.n and self.d == other.d

    def __str__(self):
        return "<Price [n={n}, d={d}]>".format(n=self.n, d=self.d)
