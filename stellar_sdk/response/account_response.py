from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from .common import Link, Flags


class Links(BaseModel):
    self: Link
    transactions: Link
    operations: Link
    payments: Link
    effects: Link
    offers: Link
    trades: Link
    data: Link


class Thresholds(BaseModel):
    low_threshold: int
    med_threshold: int
    high_threshold: int


class Balance(BaseModel):
    asset_type: str
    asset_code: Optional[str]
    asset_issuer: Optional[str]
    balance: str
    limit: Optional[str]
    buying_liabilities: str
    selling_liabilities: str
    last_modified_ledger: Optional[int]
    is_authorized: Optional[bool]
    is_authorized_to_maintain_liabilities: Optional[bool]


class Signer(BaseModel):
    weight: int
    key: str
    type: str


class AccountResponse(BaseModel):
    id: str
    account_id: str
    sequence: str
    subentry_count: int
    inflation_destination: Optional[str]
    home_domain: Optional[str]
    last_modified_ledger: int
    thresholds: Thresholds
    flags: Flags
    balances: List[Balance]
    signers: List[Signer]
    data: Dict[str, str]
    paging_token: str
    links: Links = Field(None, alias="_links")
