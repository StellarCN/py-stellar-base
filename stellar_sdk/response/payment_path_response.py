from typing import Optional, List

from pydantic import BaseModel

from .common import Asset


class PaymentPathResponse(BaseModel):
    """Represents a single payment path.
    """

    source_asset_type: str
    source_asset_code: Optional[str]
    source_asset_issuer: Optional[str]
    source_amount: str
    destination_asset_type: str
    destination_asset_code: Optional[str]
    destination_asset_issuer: Optional[str]
    destination_amount: str
    path: List[Asset]
