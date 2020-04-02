from typing import List

from pydantic import BaseModel

from .common import Price, Asset

__all__ = ["OrderbookResponse"]


class PriceLevel(BaseModel):
    """Represents an aggregation of offers that share a given price.
    """

    price: str
    price_r: Price
    amount: str


class OrderbookResponse(BaseModel):
    """Represents a snapshot summary of a given order book.
    """

    bids: List[PriceLevel]
    asks: List[PriceLevel]
    base: Asset
    counter: Asset
