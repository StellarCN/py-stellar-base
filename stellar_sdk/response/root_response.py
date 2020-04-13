from typing import Optional

from pydantic import BaseModel, Field

from .common import Link


class Links(BaseModel):
    account: Link
    accounts: Optional[Link]
    account_transactions: Link
    assets: Link
    effects: Link
    fee_stats: Link
    friendbot: Optional[Link]
    ledger: Link
    ledgers: Link
    offer: Optional[Link]
    offers: Optional[Link]
    operation: Link
    operations: Link
    order_book: Link
    payments: Link
    self: Link
    strict_receive_paths: Link
    strict_send_paths: Link
    trade_aggregations: Link
    trades: Link
    transaction: Link
    transactions: Link


class RootResponse(BaseModel):
    horizon_version: str
    core_version: str
    ingest_latest_ledger: int
    history_latest_ledger: int
    history_elder_ledger: int
    core_latest_ledger: int
    network_passphrase: str
    current_protocol_version: int
    core_supported_protocol_version: int
    links: Links = Field(None, alias="_links")
