from __future__ import annotations

import uuid
from typing import Type, TYPE_CHECKING

from .exceptions import RequestException
from .jsonrpc import *
from .soroban_rpc import *
from .. import xdr as stellar_xdr
from ..account import Account
from ..client.base_sync_client import BaseSyncClient
from ..client.requests_client import RequestsClient

if TYPE_CHECKING:
    from ..transaction_envelope import TransactionEnvelope

__all__ = ["SorobanServer"]

V = TypeVar("V")


class SorobanServer:
    def __init__(
            self,
            server_url: str = "https://horizon-futurenet.stellar.org/soroban/rpc",
            client: BaseSyncClient = None,
    ) -> None:
        self.server_url: str = server_url

        if not client:
            client = RequestsClient()
        self._client: BaseSyncClient = client

    def get_health(self) -> GetHealthResponse:
        request: Request = Request(
            id=_generate_unique_request_id(),
            method="getHealth",
        )
        return self._post(request, GetHealthResponse)

    def get_account(self, account_id: str) -> GetAccountResponse:
        request = Request[GetAccountRequest](
            id=_generate_unique_request_id(),
            method="getAccount",
            params=GetAccountRequest(address=account_id),
        )
        return self._post(request, GetAccountResponse)

    def get_events(
            self,
            start_ledger: int,
            end_ledger: int,
            filters: Sequence[EventFilter] = None,
            cursor: str = None,
            limit: int = None,
    ) -> GetEventsResponse:
        pagination = PaginationOptions(cursor=cursor, limit=limit)
        data = GetEventsRequest(
            startLedger=start_ledger,
            endLedger=end_ledger,
            filters=filters,
            pagination=pagination,
        )
        request: Request = Request[GetEventsRequest](
            id=_generate_unique_request_id(), method="getEvents", params=data
        )
        return self._post(request, GetEventsResponse)

    def get_network(self) -> GetNetworkResponse:
        request: Request = Request(
            id=_generate_unique_request_id(),
            method="getNetwork",
        )
        return self._post(request, GetNetworkResponse)

    def get_ledger_entry(self, key: stellar_xdr.LedgerKey) -> GetLedgerEntryResponse:
        # TODO: Split it into multiple points
        request = Request[GetLedgerEntryRequest](
            id=_generate_unique_request_id(),
            method="getLedgerEntry",
            params=GetLedgerEntryRequest(key=key.to_xdr()),
        )
        return self._post(request, GetLedgerEntryResponse)

    def get_transaction_status(
            self, transaction_hash: str
    ) -> GetTransactionStatusResponse:
        request = Request[GetTransactionStatusRequest](
            id=_generate_unique_request_id(),
            method="getTransactionStatus",
            params=GetTransactionStatusRequest(hash=transaction_hash),
        )
        return self._post(request, GetTransactionStatusResponse)

    def simulate_transaction(
            self, transaction_envelope: Union[TransactionEnvelope, str]
    ) -> SimulateTransactionResponse:
        xdr = (
            transaction_envelope.to_xdr()
            if isinstance(transaction_envelope, TransactionEnvelope)
            else transaction_envelope
        )
        request = Request[SimulateTransactionRequest](
            id=_generate_unique_request_id(),
            method="simulateTransaction",
            params=SimulateTransactionRequest(transaction=xdr),
        )
        # TODO: error? request.error is None, request.result.error is not None
        return self._post(request, SimulateTransactionResponse)

    def send_transaction(
            self, transaction_envelope: Union[TransactionEnvelope, str]
    ) -> SendTransactionResponse:
        xdr = transaction_envelope if isinstance(transaction_envelope, str) else transaction_envelope.to_xdr()
        request = Request[SendTransactionRequest](
            id=_generate_unique_request_id(),
            method="sendTransaction",
            params=SendTransactionRequest(transaction=xdr),
        )
        return self._post(request, SendTransactionResponse)

    def _post(self, request_body: Request, response_body_type: Type[V]) -> V:
        json_data = request_body.dict(by_alias=True)
        data = self._client.post(
            self.server_url,
            json_data=json_data,
        )
        response = Response[response_body_type, str].parse_obj(data.json())  # type: ignore[valid-type]
        if response.error:
            raise RequestException(response.error.code, response.error.message)
        return response.result  # type: ignore[return-value]

    def load_account(self, account_id: str) -> Account:
        data = self.get_account(account_id)
        return Account(account_id, data.sequence)

    def close(self) -> None:
        """Close underlying connector, and release all acquired resources."""
        self._client.close()

    def __enter__(self) -> "SorobanServer":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __str__(self):
        return f"<SorobanServer [server_url={self.server_url}, client={self._client}]>"


def _generate_unique_request_id() -> str:
    return uuid.uuid4().hex
