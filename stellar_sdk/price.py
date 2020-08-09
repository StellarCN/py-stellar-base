from .xdr import Xdr
from .utils import best_rational_approximation

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

    def to_xdr_object(self) -> Xdr.types.Price:
        """Returns the xdr object for this price object.

        :return: XDR Price object
        """
        return Xdr.types.Price(n=self.n, d=self.d)

    @classmethod
    def from_xdr_object(cls, price_xdr_object: Xdr.types.Price) -> "Price":
        """Create a :class:`Price` from an XDR Asset object.

        :param price_xdr_object: The XDR Price object.
        :return: A new :class:`Price` object from the given XDR Price object.
        """
        n = price_xdr_object.n
        d = price_xdr_object.d
        return cls(n, d)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.n == other.n and self.d == other.d

    def __str__(self):
        return f"<Price [n={self.n}, d={self.d}]>"
