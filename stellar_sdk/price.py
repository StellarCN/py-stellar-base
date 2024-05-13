from decimal import Decimal
from typing import Union

from . import xdr as stellar_xdr
from .utils import best_rational_approximation

__all__ = ["Price"]


class Price:
    """Create a new price. Price in Stellar is represented as a fraction.

    An example::

        from stellar_sdk import Price

        price_a = Price(1, 2)
        price_b = Price.from_raw_price("0.5")

    :param n: numerator
    :param d: denominator
    """

    def __init__(self, n: int, d: int) -> None:
        self.n: int = n
        self.d: int = d

    @classmethod
    def from_raw_price(cls, price: Union[str, Decimal]) -> "Price":
        """Create a :class:`Price` from the given str or Decimal price.

        :param price: the str or Decimal price. (ex. ``"0.125"``)
        :return: A new :class:`Price` object from the given str or Decimal price.
        :raises: :exc:`NoApproximationError <stellar_sdk.exceptions.NoApproximationError>`:
            if the approximation could not not be found.
        """
        best_r = best_rational_approximation(str(price))
        n = best_r["n"]
        d = best_r["d"]
        return cls(n, d)

    def to_xdr_object(self) -> stellar_xdr.Price:
        """Returns the xdr object for this price object.

        :return: XDR Price object
        """
        return stellar_xdr.Price(
            n=stellar_xdr.Int32(self.n), d=stellar_xdr.Int32(self.d)
        )

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Price) -> "Price":
        """Create a :class:`Price` from an XDR Price object.

        :param xdr_object: The XDR Price object.
        :return: A new :class:`Price` object from the given XDR Price object.
        """
        n = xdr_object.n.int32
        d = xdr_object.d.int32
        return cls(n, d)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.n * other.d) < (other.n * self.d)

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.n * other.d) <= (other.n * self.d)

    def __hash__(self):
        return hash((self.n, self.d))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.n * other.d) == (other.n * self.d)

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.n * other.d) != (other.n * self.d)

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.n * other.d) > (other.n * self.d)

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.n * other.d) >= (other.n * self.d)

    def __repr__(self):
        return f"<Price [n={self.n}, d={self.d}]>"
