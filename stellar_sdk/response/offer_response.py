from typing import Optional

from pydantic import BaseModel, Field

from .common import Link


class Links(BaseModel):
    self: Link
    offer_maker: Link


class Asset(BaseModel):
    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]


class Price(BaseModel):
    n: int
    d: int


class OfferResponse(BaseModel):
    id: int  # str in Go Impl
    paging_token: str
    seller: str
    selling: Asset
    buying: Asset
    amount: str
    price_r: Price
    price: str
    last_modified_ledger: int
    last_modified_time: str
    links: Links = Field(None, alias="_links")
