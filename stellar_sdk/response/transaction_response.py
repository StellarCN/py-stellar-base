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
    transaction: Optional[
        Link
    ]  # TODO: Temporarily include here, will be removed in the future.


class FeeBumpTransaction(BaseModel):
    """contains information about a fee bump transaction
    """

    hash: str
    signatures: List[str]


class InnerTransaction(BaseModel):
    """contains information about the inner transaction contained
    within a fee bump transaction
    """

    hash: str
    signatures: List[str]
    max_fee: int


class TransactionResponse(BaseModel):
    """Represents a single transaction.
    """

    id: str
    paging_token: str
    successful: bool
    hash: str
    ledger: int
    created_at: str
    source_account: str
    source_account_sequence: int  # str in Go impl
    fee_account: str
    fee_charged: int
    max_fee: int
    operation_count: int
    envelope_xdr: str
    result_xdr: str
    result_meta_xdr: str
    fee_meta_xdr: str
    memo_type: str
    memo: Optional[str]
    memo_bytes: Optional[str]
    signatures: List[str]
    valid_after: Optional[str]
    valid_before: Optional[str]
    fee_bump_transaction: Optional[FeeBumpTransaction]
    inner_transaction: Optional[InnerTransaction]
    links: Links = Field(None, alias="_links")
