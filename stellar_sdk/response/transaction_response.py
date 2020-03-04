from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from .common import Link


class Links(BaseModel):
    self: Link
    account: Link
    ledger: Link
    operations: Link
    effects: Link
    precedes: Link
    succeeds: Link


class TransactionResponse(BaseModel):
    """Represents a single transaction.
    """

    id: str
    paging_token: str
    successful: bool
    hash: str
    ledger: int
    created_at: datetime
    source_account: str
    source_account_sequence: int  # str in Go impl
    fee_charged: int
    max_fee: int
    operation_count: int
    envelope_xdr: str
    result_xdr: str
    result_meta_xdr: str
    fee_meta_xdr: str
    memo_type: str
    memo: Optional[str]
    signatures: List[str]
    valid_after: Optional[datetime]
    valid_before: Optional[datetime]
    links: Links = Field(None, alias="_links")
