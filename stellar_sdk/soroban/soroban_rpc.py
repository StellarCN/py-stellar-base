from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class TransactionStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"


class Cost(BaseModel):
    cpu_insns: str = Field(alias="cpuInsns")
    mem_bytes: str = Field(alias="memBytes")


class TransactionStatusResult(BaseModel):
    xdr: str


class Footprint(BaseModel):
    read_only: List[str]
    read_write: List[str]


class GetAccountResponse(BaseModel):
    id: str
    sequence: int
    # balances: List[Balance] # TODO: implement


class GetHealthResponse(BaseModel):
    status: str


class GetContractDataResponse(BaseModel):
    xdr: str
    last_modified_ledger_seq: Optional[int] = Field(alias="lastModifiedLedgerSeq")
    latest_ledger: Optional[int] = Field(alias="latestLedger")


class GetTransactionStatusResponse(BaseModel):
    id: str
    status: TransactionStatus
    results: Optional[List[TransactionStatusResult]]
    # error: Optional[jsonrpc.Error[E]]


class SendTransactionResponse(BaseModel):
    id: str
    status: TransactionStatus
    # error: Optional[jsonrpc.Error[E]]


class SimulateTransactionResponse(BaseModel):
    footprint: str
    cost: Cost
    results: Optional[List[TransactionStatusResult]]
    error: Optional[str]
    latest_ledger: int = Field(alias="latestLedger")
