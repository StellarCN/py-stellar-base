from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Sequence, TypeVar, Union

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")

Id = Union[str, int]


# JSON-RPC 2.0 definitions
class Request(BaseModel, Generic[T]):
    """Represent the request sent to Soroban-RPC.

    See `JSON-RPC 2.0 Specification - Request object <https://www.jsonrpc.org/specification#request_object>`__ for more information.
    """

    jsonrpc: str = "2.0"
    id: Id
    method: str
    params: Optional[T] = None


class Error(BaseModel):
    code: int
    message: Optional[str] = None
    data: Optional[str] = None


class Response(BaseModel, Generic[T]):
    """Represent the response returned from Soroban-RPC.

    See `JSON-RPC 2.0 Specification - Response object <https://www.jsonrpc.org/specification#response_object>`__ for more information.
    """

    jsonrpc: str
    id: Id
    result: Optional[T] = None
    error: Optional[Error] = None


# get_events
class EventFilterType(Enum):
    SYSTEM = "system"
    CONTRACT = "contract"
    DIAGNOSTIC = "diagnostic"


class EventFilter(BaseModel):
    event_type: Optional[EventFilterType] = Field(alias="type", default=None)
    contract_ids: Optional[Sequence[str]] = Field(alias="contractIds", default=None)
    topics: Optional[Sequence[Sequence[str]]] = None
    model_config = ConfigDict(populate_by_name=True)


class EventInfo(BaseModel):
    event_type: str = Field(alias="type")
    ledger: int = Field(alias="ledger")
    ledger_close_at: datetime = Field(alias="ledgerClosedAt")
    contract_id: str = Field(alias="contractId")
    id: str = Field(alias="id")
    paging_token: str = Field(alias="pagingToken")
    topic: List[str] = Field(alias="topic")
    value: str = Field(alias="value")
    in_successful_contract_call: bool = Field(alias="inSuccessfulContractCall")
    transaction_hash: str = Field(alias="txHash")


class PaginationOptions(BaseModel):
    cursor: Optional[str] = None
    limit: Optional[int] = None


class GetEventsRequest(BaseModel):
    """Response for JSON-RPC method getEvents.

    See `getEvents documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getEvents>`__ for
    more information.
    """

    start_ledger: int = Field(alias="startLedger")
    filters: Optional[Sequence[EventFilter]] = None
    pagination: Optional[PaginationOptions] = None


class GetEventsResponse(BaseModel):
    """Response for JSON-RPC method getEvents.

    See `getEvents documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getEvents>`__ for
    more information.
    """

    events: List[EventInfo] = Field(alias="events")
    latest_ledger: int = Field(alias="latestLedger")


# get_ledger_entries
class GetLedgerEntriesRequest(BaseModel):
    """Response for JSON-RPC method getLedgerEntries.

    See `getLedgerEntries documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getLedgerEntries>`__ for
    more information."""

    keys: Sequence[str]


class LedgerEntryResult(BaseModel):
    key: str
    xdr: str
    last_modified_ledger: int = Field(alias="lastModifiedLedgerSeq")
    live_until_ledger: Optional[int] = Field(alias="liveUntilLedgerSeq", default=None)


class GetLedgerEntriesResponse(BaseModel):
    """Response for JSON-RPC method getLedgerEntries.

    See `getLedgerEntries documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getLedgerEntries>`__ for
    more information."""

    entries: Optional[List[LedgerEntryResult]] = None
    latest_ledger: int = Field(alias="latestLedger")


# get_network
class GetNetworkResponse(BaseModel):
    """Response for JSON-RPC method getNetwork.

    See `getNetwork documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getNetwork>`__ for
    more information."""

    friendbot_url: Optional[str] = Field(alias="friendbotUrl", default=None)
    passphrase: str
    protocol_version: int = Field(alias="protocolVersion")


# health
class GetHealthResponse(BaseModel):
    """Response for JSON-RPC method getHealth.

    See `getHealth documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getHealth>`__ for
    more information.
    """

    status: str
    latest_ledger: int = Field(alias="latestLedger")
    oldest_ledger: int = Field(alias="oldestLedger")
    ledger_retention_window: int = Field(alias="ledgerRetentionWindow")


# simulate_transaction
class ResourceConfig(BaseModel):
    """ResourceConfig represents the additional resource leeways for transaction simulation."""

    instruction_lee_way: int = Field(alias="instructionLeeway")
    model_config = ConfigDict(populate_by_name=True)


class SimulateTransactionRequest(BaseModel):
    """Response for JSON-RPC method simulateTransaction.

    .. note::
        The simulation response will have different model representations with different
        members present or absent depending on type of response that it is conveying. For example, the
        simulation response for invoke host function, could be one of three types: error, success, or
        restore operation needed.

    See `simulateTransaction documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/simulateTransaction>`__ for
    more information.
    """

    transaction: str
    resource_config: Optional[ResourceConfig] = Field(
        alias="resourceConfig", default=None
    )
    model_config = ConfigDict(populate_by_name=True)


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


class RestorePreamble(BaseModel):
    transaction_data: str = Field(alias="transactionData")
    min_resource_fee: int = Field(alias="minResourceFee")


class LedgerEntryChange(BaseModel):
    """LedgerEntryChange designates a change in a ledger entry. Before and After cannot be omitted at the same time.
    If Before is omitted, it constitutes a creation, if After is omitted, it constitutes a deletion.
    """

    # LedgerEntryChangeType
    type: str
    # LedgerEntryKey in base64
    key: str
    # LedgerEntry XDR in base64
    before: Optional[str] = None
    # LedgerEntry XDR in base64
    after: Optional[str] = None


class SimulateTransactionResponse(BaseModel):
    """Response for JSON-RPC method simulateTransaction.

    See `simulateTransaction documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/simulateTransaction>`__ for
    more information."""

    error: Optional[str] = None
    transaction_data: Optional[str] = Field(alias="transactionData", default=None)
    # SorobanTransactionData XDR in base64
    min_resource_fee: Optional[int] = Field(alias="minResourceFee", default=None)
    events: Optional[List[str]] = None
    # DiagnosticEvent XDR in base64
    results: Optional[List[SimulateHostFunctionResult]] = None
    # an array of the individual host function call results.
    # This will only contain a single element if present, because only a single invokeHostFunctionOperation
    # is supported per transaction.
    cost: Optional[SimulateTransactionCost] = None
    # the effective cpu and memory cost of the invoked transaction execution.
    restore_preamble: Optional[RestorePreamble] = Field(
        alias="restorePreamble", default=None
    )
    # If present, it indicates how the state (ledger entries) will change as a result of the transaction execution.
    state_changes: Optional[List[LedgerEntryChange]] = Field(
        alias="stateChanges", default=None
    )
    # If present, it indicates that a prior RestoreFootprint is required
    latest_ledger: int = Field(alias="latestLedger")


# get_transaction_status
class GetTransactionStatus(Enum):
    SUCCESS = "SUCCESS"
    """indicates the transaction was included in the ledger and it was executed without errors."""
    NOT_FOUND = "NOT_FOUND"
    """indicates the transaction was not found in Soroban-RPC's transaction store."""
    FAILED = "FAILED"
    """TransactionStatusFailed indicates the transaction was included in the ledger and it was executed with an error."""


class TransactionResponseError(BaseModel):
    code: str
    message: str
    data: Dict[str, Any]


class GetTransactionRequest(BaseModel):
    """Response for JSON-RPC method getTransaction.

    See `getTransaction documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getTransaction>`__ for
    more information."""

    hash: str


class GetTransactionResponse(BaseModel):
    """Response for JSON-RPC method getTransaction.

    See `getTransaction documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getTransaction>`__ for
    more information."""

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
    create_at: Optional[int] = Field(alias="createdAt", default=None)


# send_transaction
class SendTransactionStatus(Enum):
    ERROR = "ERROR"
    """represents the status value returned by stellar-core when an error occurred from submitting a transaction"""
    PENDING = "PENDING"
    """represents the status value returned by stellar-core when a transaction has been accepted for processing"""
    DUPLICATE = "DUPLICATE"
    """represents the status value returned by stellar-core when a submitted transaction is a duplicate"""
    TRY_AGAIN_LATER = "TRY_AGAIN_LATER"
    """represents the status value returned by stellar-core when a submitted transaction was not included in the previous 4 ledgers and get banned for being added in the next few ledgers."""


class SendTransactionRequest(BaseModel):
    """Response for JSON-RPC method sendTransaction.

    See `sendTransaction documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/sendTransaction>`__ for
    more information."""

    transaction: str


class SendTransactionResponse(BaseModel):
    """Response for JSON-RPC method sendTransaction.

    See `sendTransaction documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/sendTransaction>`__ for
    more information."""

    error_result_xdr: Optional[str] = Field(alias="errorResultXdr", default=None)
    diagnostic_events_xdr: Optional[List[str]] = Field(
        alias="diagnosticEventsXdr", default=None
    )
    status: SendTransactionStatus = Field(alias="status")
    hash: str = Field(alias="hash")
    latest_ledger: int = Field(alias="latestLedger")
    latest_ledger_close_time: int = Field(alias="latestLedgerCloseTime")


# get_latest_ledger
class GetLatestLedgerResponse(BaseModel):
    """Response for JSON-RPC method getLatestLedger.

    See `getLatestLedger documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getLatestLedger>`__ for
    more information."""

    id: str
    protocol_version: int = Field(alias="protocolVersion")
    sequence: int


# get_fee_stats
class FeeDistribution(BaseModel):
    max: int
    min: int
    mode: int
    p10: int
    p20: int
    p30: int
    p40: int
    p50: int
    p60: int
    p70: int
    p80: int
    p90: int
    p95: int
    p99: int
    transaction_count: int = Field(alias="transactionCount")
    ledger_count: int = Field(alias="ledgerCount")


class GetFeeStatsResponse(BaseModel):
    """Response for JSON-RPC method getFeeStats.

    See `getFeeStats documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getFeeStats>`__ for
    more information."""

    soroban_inclusion_fee: FeeDistribution = Field(alias="sorobanInclusionFee")
    inclusion_fee: FeeDistribution = Field(alias="inclusionFee")
    latest_ledger: int = Field(alias="latestLedger")


# get_transactions
class GetTransactionsRequest(BaseModel):
    """Request for JSON-RPC method getTransactions.

    See `getTransactions documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getTransactions>`__ for
    more information."""

    start_ledger: int = Field(alias="startLedger")
    pagination: Optional[PaginationOptions] = None


class Transaction(BaseModel):
    status: str
    application_order: int = Field(alias="applicationOrder")
    fee_bump: bool = Field(alias="feeBump")
    envelope_xdr: str = Field(alias="envelopeXdr")
    result_xdr: str = Field(alias="resultXdr")
    result_meta_xdr: str = Field(alias="resultMetaXdr")
    ledger: int
    created_at: int = Field(alias="createdAt")
    diagnostic_events_xdr: Optional[List[str]] = Field(
        alias="diagnosticEventsXdr", default=None
    )


class GetTransactionsResponse(BaseModel):
    """Response for JSON-RPC method getTransactions.

    See `getTransactions documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getTransactions>`__ for
    more information."""

    transactions: List[Transaction]
    latest_ledger: int = Field(alias="latestLedger")
    latest_ledger_close_timestamp: int = Field(alias="latestLedgerCloseTimestamp")
    oldest_ledger: int = Field(alias="oldestLedger")
    oldest_ledger_close_timestamp: int = Field(alias="oldestLedgerCloseTimestamp")
    cursor: str


# get_version_info
# TODO: To avoid breaking change, let's add it later.
# See: https://github.com/stellar/soroban-rpc/pull/164
# class GetVersionInfoResponse(BaseModel):
#     """Response for JSON-RPC method getVersionInfo.
#
#     See `getVersionInfo documentation <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getVersionInfo>`__ for
#     more information."""
#
#     version: str
#     commit_hash: str = Field(alias="commitHash")
#     build_time_stamp: str = Field(alias="buildTimeStamp")
#     captive_core_version: str = Field(alias="captiveCoreVersion")
#     protocol_version: int = Field(alias="protocolVersion")
