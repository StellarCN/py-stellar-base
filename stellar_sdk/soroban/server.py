import uuid
from typing import Type

from .exceptions import RequestException
from .jsonrpc import *
from .soroban_rpc import *
from .. import xdr as stellar_xdr
from ..client.base_sync_client import BaseSyncClient
from ..client.requests_client import RequestsClient
from ..transaction_envelope import TransactionEnvelope
from ..type_checked import type_checked

__all__ = ["SorobanServer"]

V = TypeVar("V")


@type_checked
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

    def get_account(self, address: str) -> GetAccountResponse:
        request = Request[List[str]](
            id=_generate_unique_request_id(),
            method="getAccount",
            params=[address],
        )
        return self._post(request, GetAccountResponse)

    def get_contract_data(
        self, contract_id: str, key: stellar_xdr.SCVal
    ) -> GetContractDataResponse:
        request = Request[List[str]](
            id=_generate_unique_request_id(),
            method="getContractData",
            params=[contract_id, key.to_xdr()],
        )
        return self._post(request, GetContractDataResponse)

    def get_transaction_status(
        self, transaction_hash: str
    ) -> GetTransactionStatusResponse:
        request = Request[List[str]](
            id=_generate_unique_request_id(),
            method="getTransactionStatus",
            params=[transaction_hash],
        )
        return self._post(request, GetTransactionStatusResponse)

    def simulate_transaction(
        self, transaction_envelope: TransactionEnvelope
    ) -> SimulateTransactionResponse:
        request = Request[List[str]](
            id=_generate_unique_request_id(),
            method="simulateTransaction",
            params=[transaction_envelope.to_xdr()],
        )
        # TODO: error? request.error is None, request.result.error is not None
        return self._post(request, SimulateTransactionResponse)

    def send_transaction(
        self, transaction_envelope: TransactionEnvelope
    ) -> SendTransactionResponse:
        request = Request[List[str]](
            id=_generate_unique_request_id(),
            method="sendTransaction",
            params=[transaction_envelope.to_xdr()],
        )
        return self._post(request, SendTransactionResponse)

    def _post(self, request_body: Request, response_body_type: Type[V]) -> V:
        data = self._client.post(
            self.server_url,
            json_data=request_body.dict(),
        )
        response = Response[response_body_type, str].parse_obj(data.json())  # type: ignore[valid-type]
        if response.error:
            raise RequestException(response.error.code, response.error.message)
        return response.result  # type: ignore[return-value]

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
