from typing import Optional

from pydantic import BaseModel, Field

from .common import Link, Price


class Links(BaseModel):
    self: Link
    base: Link
    counter: Link
    operation: Link


class TradeResponse(BaseModel):
    """Represents a single Trade.
    """

    id: str
    paging_token: str
    ledger_close_time: str
    offer_id: str
    base_offer_id: str
    base_account: str
    base_amount: str
    base_asset_type: str
    base_asset_code: Optional[str]
    base_asset_issuer: Optional[str]
    counter_offer_id: str
    counter_account: str
    counter_amount: str
    counter_asset_type: str
    counter_asset_code: Optional[str]
    counter_asset_issuer: Optional[str]
    base_is_seller: bool
    price: Price
    links: Links = Field(None, alias="_links")
