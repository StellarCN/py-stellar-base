from decimal import Decimal
from fractions import Fraction

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
    :raises: :exc:`ValueError`: if ``n`` or ``d`` is not positive, as the network
        requires.
    """

    def __init__(self, n: int, d: int) -> None:
        if n <= 0 or d <= 0:
            raise ValueError(
                f"A price needs a positive numerator and denominator, not {n}/{d}."
            )
        self.n: int = n
        self.d: int = d

    @classmethod
    def from_raw_price(cls, price: str | Decimal) -> "Price":
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
        return stellar_xdr.Price(n=self.n, d=self.d)

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Price) -> "Price":
        """Create a :class:`Price` from an XDR Price object.

        :param xdr_object: The XDR Price object.
        :return: A new :class:`Price` object from the given XDR Price object.
        """
        return cls(xdr_object.n, xdr_object.d)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.n * other.d) < (other.n * self.d)

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.n * other.d) <= (other.n * self.d)

    def __hash__(self):
        # Equal prices are the same fraction, such as 1/2 and 2/4.
        return hash(Fraction(self.n, self.d))

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
