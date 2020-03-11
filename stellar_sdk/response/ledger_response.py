from typing import Optional

from pydantic import BaseModel, Field

from .common import Link


class Links(BaseModel):
    self: Link
    transactions: Link
    operations: Link
    payments: Link
    effects: Link


class LedgerResponse(BaseModel):
    id: str
    paging_token: str
    hash: str
    prev_hash: Optional[str]
    sequence: int
    successful_transaction_count: int
    failed_transaction_count: int
    operation_count: int
    closed_at: str
    total_coins: str
    fee_pool: str
    base_fee_in_stroops: int
    base_reserve_in_stroops: int
    max_tx_set_size: int
    protocol_version: int
    header_xdr: str
    links: Links = Field(None, alias="_links")
