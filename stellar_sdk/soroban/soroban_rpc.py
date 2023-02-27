from datetime import datetime
from enum import Enum
from typing import Sequence, Optional, List, Dict, Any

from pydantic import BaseModel, Field

from ..xdr.sc_val import SCVal as XdrSCVal


# account
class GetAccountRequest(BaseModel):
    address: str


class GetAccountResponse(BaseModel):
    id: str
    sequence: int


# get_events
class SegmentFilter(BaseModel):
    wildcard: Optional[str]
    scval: Optional[XdrSCVal]

    class Config:
        json_encoders = {
            XdrSCVal: lambda v: v.to_xdr(),
        }
        arbitrary_types_allowed = True


class EventFilter(BaseModel):
    event_type: Optional[str] = Field(alias="type")
    contract_ids: Optional[List[str]] = Field(alias="contractIds")
    topics: Optional[List[List[SegmentFilter]]]


class EventInfoValue(BaseModel):
    xdr: str


class EventInfo(BaseModel):
    event_type: str = Field(alias="type")
    ledger: int = Field(alias="ledger")
    ledger_close_at: datetime = Field(alias="ledgerClosedAt")
    contract_id: str = Field(alias="contractId")
    id: str = Field(alias="id")
    paging_token: str = Field(alias="pagingToken")
    topic: Sequence[str] = Field(alias="topic")
    value: EventInfoValue = Field(alias="value")


class PaginationOptions(BaseModel):
    cursor: Optional[str]
    limit: Optional[int]


class GetEventsRequest(BaseModel):
    start_ledger: str = Field(alias="startLedger")
    end_ledger: str = Field(alias="endLedger")  # TODO: check it
    filters: Optional[List[EventFilter]]
    pagination: Optional[PaginationOptions]


class GetEventsResponse(BaseModel):
    events: Sequence[EventInfo] = Field(alias="events")
    latest_ledger: int = Field(alias="latestLedger")


# get_ledger_entry
class GetLedgerEntryRequest(BaseModel):
    key: str


class GetLedgerEntryResponse(BaseModel):
    xdr: str
    last_modified_ledger_seq: int = Field(alias="lastModifiedLedgerSeq")
    latest_ledger: int = Field(alias="latestLedger")


# get_network
class GetNetworkResponse(BaseModel):
    friendbot_url: Optional[str] = Field(alias="friendbotUrl")
    passphrase: str
    protocol_version: int = Field(alias="protocolVersion")


# health
class GetHealthResponse(BaseModel):
    status: str


# simulate_transaction
class SimulateTransactionRequest(BaseModel):
    transaction: str


class SimulateTransactionCost(BaseModel):
    cpu_insns: int = Field(alias="cpuInsns")
    mem_bytes: int = Field(alias="memBytes")


class SimulateTransactionResult(BaseModel):
    auth: Optional[List[str]]
    footprint: str
    xdr: str


class SimulateTransactionResponse(BaseModel):
    error: Optional[str]
    results: Optional[List[SimulateTransactionResult]]
    cost: SimulateTransactionCost
    latest_ledger: int = Field(alias="latestLedger")


# get_transaction_status
class TransactionStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"


class TransactionResponseError(BaseModel):
    code: str
    message: str
    data: Dict[str, Any]


class SCVal(BaseModel):
    xdr: str


class GetTransactionStatusRequest(BaseModel):
    hash: str


class GetTransactionStatusResponse(BaseModel):
    id: str
    status: TransactionStatus
    envelope_xdr: Optional[str] = Field(alias="envelopeXdr")
    result_xdr: Optional[str] = Field(alias="resultXdr")
    result_meta_xdr: Optional[str] = Field(alias="resultMetaXdr")
    results: Optional[List[SCVal]]
    # error will be empty unless status is equal to "error"
    error: Optional[TransactionResponseError]


# send_transaction
class SendTransactionRequest(BaseModel):
    transaction: str


class SendTransactionResponse(BaseModel):
    id: str
    status: TransactionStatus
    # error will be empty unless status is equal to "error"
    error: Optional[TransactionResponseError]
