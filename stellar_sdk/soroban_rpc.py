from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Sequence, TypeVar, Union

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")

Id = Union[str, int]


# JSON-RPC 2.0 definitions
class Request(BaseModel, Generic[T]):
    jsonrpc: str = "2.0"
    id: Id
    method: str
    params: Optional[T] = None


class Error(BaseModel):
    code: int
    message: Optional[str] = None
    data: Optional[str] = None


class Response(BaseModel, Generic[T]):
    jsonrpc: str
    id: Id
    result: Optional[T] = None
    error: Optional[Error] = None


# account
class GetAccountRequest(BaseModel):
    address: str


class GetAccountResponse(BaseModel):
    id: str
    sequence: int


# get_events


class EventFilterType(Enum):
    SYSTEM = "system"
    CONTRACT = "contract"
    DIAGNOSTIC = "diagnostic"


class EventFilter(BaseModel):
    event_type: Optional[EventFilterType] = Field(alias="type", default=None)
    contract_ids: Optional[List[str]] = Field(alias="contractIds", default=None)
    topics: Optional[List[List[str]]] = None
    model_config = ConfigDict(populate_by_name=True)


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
    in_successful_contract_call: bool = Field(alias="inSuccessfulContractCall")


class PaginationOptions(BaseModel):
    cursor: Optional[str] = None
    limit: Optional[int] = None


class GetEventsRequest(BaseModel):
    start_ledger: str = Field(alias="startLedger")
    filters: Optional[Sequence[EventFilter]] = None
    pagination: Optional[PaginationOptions] = None


class GetEventsResponse(BaseModel):
    events: Sequence[EventInfo] = Field(alias="events")
    latest_ledger: int = Field(alias="latestLedger")


# get_ledger_entries
class GetLedgerEntriesRequest(BaseModel):
    keys: List[str]


class LedgerEntryResult(BaseModel):
    key: str
    xdr: str
    last_modified_ledger_seq: int = Field(alias="lastModifiedLedgerSeq")


class GetLedgerEntriesResponse(BaseModel):
    entries: Optional[List[LedgerEntryResult]] = None
    latest_ledger: int = Field(alias="latestLedger")


# get_network
class GetNetworkResponse(BaseModel):
    friendbot_url: Optional[str] = Field(alias="friendbotUrl", default=None)
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
    auth: Optional[List[str]] = None
    events: Optional[List[str]] = None
    footprint: str
    xdr: str


class SimulateHostFunctionResult(BaseModel):
    auth: Optional[List[str]] = None
    xdr: str


class SimulateTransactionResponse(BaseModel):
    error: Optional[str] = None
    # Empty string?
    transaction_data: str = Field(alias="transactionData")
    events: Optional[List[str]] = None
    min_resource_fee: int = Field(alias="minResourceFee")
    results: Optional[List[SimulateHostFunctionResult]] = None
    cost: SimulateTransactionCost
    latest_ledger: int = Field(alias="latestLedger")


# get_transaction_status
class GetTransactionStatus(Enum):
    SUCCESS = "SUCCESS"  # "indicates the transaction was included in the ledger and it was executed without errors.",
    NOT_FOUND = "NOT_FOUND"  # "indicates the transaction was not found in Soroban-RPC's transaction store.",
    FAILED = "FAILED"  # "TransactionStatusFailed indicates the transaction was included in the ledger and it was executed with an error.",


class TransactionResponseError(BaseModel):
    code: str
    message: str
    data: Dict[str, Any]


class GetTransactionRequest(BaseModel):
    hash: str


class GetTransactionResponse(BaseModel):
    status: GetTransactionStatus
    latest_ledger: int = Field(alias="latestLedger")
    latest_ledger_close_time: int = Field(alias="latestLedgerCloseTime")
    oldest_ledger: int = Field(alias="oldestLedger")
    oldest_ledger_close_time: int = Field(alias="oldestLedgerCloseTime")
    # The fields below are only present if Status is not TransactionStatus.NOT_FOUND.
    application_order: Optional[int] = Field(alias="applicationOrder", default=None)
    fee_bump: Optional[bool] = Field(alias="feeBump", default=None)
    envelope_xdr: Optional[str] = Field(
        alias="envelopeXdr", default=None
    )  # stellar_sdk.xdr.TransactionEnvelope
    result_xdr: Optional[str] = Field(
        alias="resultXdr", default=None
    )  # stellar_sdk.xdr.TransactionResult
    result_meta_xdr: Optional[str] = Field(
        alias="resultMetaXdr", default=None
    )  # stellar_sdk.xdr.TransactionMeta
    ledger: Optional[int] = Field(alias="ledger", default=None)
    ledger_close_time: Optional[int] = Field(alias="ledgerCloseTime", default=None)


# send_transaction
class SendTransactionStatus(Enum):
    ERROR = "ERROR"  # represents the status value returned by stellar-core when an error occurred from submitting a transaction
    PENDING = "PENDING"  # represents the status value returned by stellar-core when a transaction has been accepted for processing
    DUPLICATE = "DUPLICATE"  # represents the status value returned by stellar-core when a submitted transaction is a duplicate
    TRY_AGAIN_LATER = "TRY_AGAIN_LATER"  # represents the status value returned by stellar-core when a submitted transaction was not included in the previous 4 ledgers and get banned for being added in the next few ledgers.


class SendTransactionRequest(BaseModel):
    transaction: str


class SendTransactionResponse(BaseModel):
    error_result_xdr: Optional[str] = Field(alias="errorResultXdr", default=None)
    status: SendTransactionStatus = Field(alias="status")
    hash: str = Field(alias="hash")
    latest_ledger: int = Field(alias="latestLedger")
    latest_ledger_close_time: int = Field(alias="latestLedgerCloseTime")


# get_latest_ledger
class GetLatestLedgerResponse(BaseModel):
    id: str
    protocol_version: int = Field(alias="protocolVersion")
    sequence: int
