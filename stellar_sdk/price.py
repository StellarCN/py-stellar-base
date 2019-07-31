from .utils import best_rational_approximation
from .stellarxdr import Xdr


class Price:
    def __init__(self, n: int, d: int) -> None:
        self.n = n
        self.d = d

    @classmethod
    def from_raw_price(cls, price: str) -> 'Price':
        best_r = best_rational_approximation(price)
        n = best_r['n']
        d = best_r['d']
        return cls(n, d)

    def to_xdr_object(self) -> Xdr.types.Price:
        return Xdr.types.Price(n=self.n, d=self.d)

    @classmethod
    def from_xdr_object(cls, price_xdr_object: Xdr.types.Price) -> 'Price':
        n = price_xdr_object.n
        d = price_xdr_object.d
        return cls(n, d)

    def __eq__(self, other: 'Price') -> bool:
        return self.n == other.n and self.d == other.d
