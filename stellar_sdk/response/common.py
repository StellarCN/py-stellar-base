from typing import Optional

from pydantic import BaseModel


class Asset(BaseModel):
    """Represents an asset.
    """

    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]


class Flags(BaseModel):
    auth_required: bool
    auth_revocable: bool
    auth_immutable: bool


class Link(BaseModel):
    href: str
    templated: Optional[bool]


class Price(BaseModel):
    """Represents a price.
    """

    n: int
    d: int
