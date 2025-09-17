from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Type

from pydantic import BaseModel

from . import scval
from . import xdr as stellar_xdr
from .account import Account
from .address import Address
from .asset import Asset
from .base_soroban_server import (
    Durability,
    ResourceLeeway,
    _assemble_transaction,
    _generate_unique_request_id,
)
from .client.requests_client import RequestsClient
from .exceptions import (
    AccountNotFoundException,
    PrepareTransactionException,
    SorobanRpcErrorResponse,
)
from .keypair import Keypair
from .soroban_rpc import *
from .strkey import StrKey
from .xdr import (
    ContractDataDurability,
    LedgerEntryData,
    LedgerEntryType,
    LedgerKey,
    LedgerKeyContractData,
)

if TYPE_CHECKING:
    from .client.base_sync_client import BaseSyncClient
    from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
    from .transaction_envelope import TransactionEnvelope

__all__ = ["SorobanServer", "Durability"]

V = TypeVar("V", bound=BaseModel)


class SorobanServer:
    """Server handles the network connection to a Soroban RPC instance and
    exposes an interface for requests to that instance.

    :param server_url: Soroban RPC server URL. (ex. ``https://soroban-testnet.stellar.org:443``)
    :param client: A client instance that will be used to make requests.
    """

    def __init__(
        self,
        server_url: str = "https://soroban-testnet.stellar.org:443",
        client: Optional[BaseSyncClient] = None,
    ) -> None:
        self.server_url: str = server_url

        if not client:
            client = RequestsClient()
        self._client: BaseSyncClient = client

    def get_health(self) -> GetHealthResponse:
        """General node health check.

        See `Soroban RPC Documentation - getHealth <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getHealth>`_

        :return: A :class:`GetHealthResponse <stellar_sdk.soroban_rpc.GetHealthResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        request: Request = Request(
            id=_generate_unique_request_id(),
            method="getHealth",
            params=None,
        )
        return self._post(request, GetHealthResponse)

    def get_events(
        self,
        start_ledger: Optional[int] = None,
        end_ledger: Optional[int] = None,
        filters: Optional[Sequence[EventFilter]] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> GetEventsResponse:
        """Fetch a list of events that occurred in the ledger range.

        See `Soroban RPC Documentation - getEvents <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getEvents>`_

        :param start_ledger: Ledger sequence number to start fetching responses from (inclusive). This method will return an error if startLedger is less than the oldest ledger stored in this node, or greater than the latest ledger seen by this node. If a cursor is included in the request, startLedger must be omitted.
        :param end_ledger: Ledger sequence number represents the end of search window (exclusive). If a cursor is included in the request, this must be omitted.
        :param filters: A list of filters to apply to the results.
        :param cursor: A cursor value for use in pagination.
        :param limit: The maximum number of records to return.
        :return: A :class:`GetEventsResponse <stellar_sdk.soroban_rpc.GetEventsResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
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
        """General info about the currently configured network.

        See `Soroban RPC Documentation - getNetwork <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getNetwork>`_

        :return: A :class:`GetNetworkResponse <stellar_sdk.soroban_rpc.GetNetworkResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        request: Request = Request(
            id=_generate_unique_request_id(),
            method="getNetwork",
            params=None,
        )
        return self._post(request, GetNetworkResponse)

    def get_latest_ledger(self) -> GetLatestLedgerResponse:
        """Fetches the latest ledger meta info from network which Soroban-RPC is connected to.

        See `Soroban RPC Documentation - getLatestLedger <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getLatestLedger>`_

        :return: A :class:`GetLatestLedgerResponse <stellar_sdk.soroban_rpc.GetLatestLedgerResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        request: Request = Request(
            id=_generate_unique_request_id(),
            method="getLatestLedger",
            params=None,
        )
        return self._post(request, GetLatestLedgerResponse)

    def get_ledger_entries(
        self, keys: List[stellar_xdr.LedgerKey]
    ) -> GetLedgerEntriesResponse:
        """For reading the current value of ledger entries directly.

        Allows you to directly inspect the current state of a contract, a contract's code,
        or any other ledger entry. This is a backup way to access your contract data
        which may not be available via events or simulateTransaction.

        See `Soroban RPC Documentation - getLedgerEntries <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getLedgerEntries>`_

        :param keys: The ledger keys to fetch.
        :return: A :class:`GetLedgerEntriesResponse <stellar_sdk.soroban_rpc.GetLedgerEntriesResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        request = Request[GetLedgerEntriesRequest](
            id=_generate_unique_request_id(),
            method="getLedgerEntries",
            params=GetLedgerEntriesRequest(keys=[key.to_xdr() for key in keys]),
        )
        return self._post(request, GetLedgerEntriesResponse)

    def get_transaction(self, transaction_hash: str) -> GetTransactionResponse:
        """Fetch the specified transaction.

        See `Soroban RPC Documentation - getTransaction <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getTransaction>`_

        :param transaction_hash: The hash of the transaction to fetch.
        :return: A :class:`GetTransactionResponse <stellar_sdk.soroban_rpc.GetTransactionResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        request = Request[GetTransactionRequest](
            id=_generate_unique_request_id(),
            method="getTransaction",
            params=GetTransactionRequest(hash=transaction_hash),
        )
        return self._post(request, GetTransactionResponse)

    def simulate_transaction(
        self,
        transaction_envelope: TransactionEnvelope,
        addl_resources: Optional[ResourceLeeway] = None,
        auth_mode: Optional[AuthMode] = None,
    ) -> SimulateTransactionResponse:
        """Submit a trial contract invocation to get back return values, expected ledger footprint, and expected costs.

        See `Soroban RPC Documentation - simulateTransaction <https://developers.stellar.org/docs/data/rpc/api-reference/methods/simulateTransaction>`_

        :param transaction_envelope: The transaction to simulate. It should include exactly one operation,
            which must be one of :class:`RestoreFootprint <stellar_sdk.operation.RestoreFootprintOperation>`,
            :class:`InvokeHostFunction <stellar_sdk.operation.InvokeHostFunction>` or
            :class:`ExtendFootprintTTL <stellar_sdk.operation.RestoreFootprint>` operation.
            Any provided footprint will be ignored.
        :param addl_resources: Additional resource include in the simulation.
        :param auth_mode: Explicitly allows users to opt-in to non-root authorization in recording mode.
        :return: A :class:`SimulateTransactionResponse <stellar_sdk.soroban_rpc.SimulateTransactionResponse>` object
            contains the cost, footprint, result/auth requirements (if applicable), and error of the transaction.
        """
        xdr = (
            transaction_envelope
            if isinstance(transaction_envelope, str)
            else transaction_envelope.to_xdr()
        )
        resource_config = None
        if addl_resources:
            resource_config = ResourceConfig(
                instructionLeeway=addl_resources.cpu_instructions,
            )

        request = Request[SimulateTransactionRequest](
            id=_generate_unique_request_id(),
            method="simulateTransaction",
            params=SimulateTransactionRequest(
                transaction=xdr, resourceConfig=resource_config, authMode=auth_mode
            ),
        )
        return self._post(request, SimulateTransactionResponse)

    def send_transaction(
        self,
        transaction_envelope: Union[
            TransactionEnvelope, FeeBumpTransactionEnvelope, str
        ],
    ) -> SendTransactionResponse:
        """Submit a real transaction to the Stellar network. This is the only way to make changes "on-chain".

        See `Soroban RPC Documentation - sendTransaction <https://developers.stellar.org/docs/data/rpc/api-reference/methods/sendTransaction>`_

        :param transaction_envelope: The transaction to send.
        :return: A :class:`SendTransactionResponse <stellar_sdk.soroban_rpc.SendTransactionResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        xdr = (
            transaction_envelope
            if isinstance(transaction_envelope, str)
            else transaction_envelope.to_xdr()
        )
        request = Request[SendTransactionRequest](
            id=_generate_unique_request_id(),
            method="sendTransaction",
            params=SendTransactionRequest(transaction=xdr),
        )
        return self._post(request, SendTransactionResponse)

    def poll_transaction(
        self,
        transaction_hash: str,
        max_attempts: int = DEFAULT_POLLING_ATTEMPTS,
        sleep_strategy: SleepStrategy = BasicSleepStrategy,
    ) -> GetTransactionResponse:
        """Poll for a particular transaction with certain parameters.

        After submitting a transaction, clients can use this to poll for transaction completion and return a definitive state of success or failure.

        :param transaction_hash: The hash of the transaction to poll for.
        :param max_attempts: The number of attempts to make before returning the last-seen status, defaults to 30.
        :param sleep_strategy: The amount of time to wait for between each attempt, defaults to 1 second between each attempt.
        :return: A :class:`GetTransactionResponse <stellar_sdk.soroban_rpc.GetTransactionResponse>` response object after a "found" response, (which may be success or failure) or the last response obtained after polling the maximum number of specified attempts.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        if max_attempts < 1:
            raise ValueError("max_attempts must be greater than 0")
        attempt: int = 0

        while resp := self.get_transaction(transaction_hash=transaction_hash):
            if resp.status != GetTransactionStatus.NOT_FOUND:
                return resp

            attempt += 1
            if attempt >= max_attempts:
                break

            time.sleep(sleep_strategy(attempt))
        return resp

    def get_fee_stats(self) -> GetFeeStatsResponse:
        """General info about the fee stats.

        See `Soroban RPC Documentation - getFeeStats <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getFeeStats>`_

        :return: A :class:`GetFeeStatsResponse <stellar_sdk.soroban_rpc.GetFeeStatsResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        request: Request = Request(
            id=_generate_unique_request_id(),
            method="getFeeStats",
            params=None,
        )
        return self._post(request, GetFeeStatsResponse)

    def get_transactions(
        self,
        start_ledger: Optional[int] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> GetTransactionsResponse:
        """Fetch a detailed list of transactions starting from the user specified starting point that you can paginate
        as long as the pages fall within the history retention of their corresponding RPC provider.

        See `Soroban RPC Documentation - getTransactions <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getTransactions>`_

        :param start_ledger: The first ledger to include in the results.
        :param cursor: A cursor value for use in pagination.
        :param limit: The maximum number of records to return.
        :return: A :class:`GetTransactionsResponse <stellar_sdk.soroban_rpc.GetTransactionsResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        pagination = PaginationOptions(cursor=cursor, limit=limit)
        data = GetTransactionsRequest(
            startLedger=start_ledger,
            pagination=pagination,
        )
        request: Request = Request[GetTransactionsRequest](
            id=_generate_unique_request_id(), method="getTransactions", params=data
        )
        return self._post(request, GetTransactionsResponse)

    def get_ledgers(
        self,
        start_ledger: Optional[int] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> GetLedgersResponse:
        """Fetch a detailed list of ledgers starting from the user specified starting point that you can paginate
        as long as the pages fall within the history retention of their corresponding RPC provider.

        See `Soroban RPC Documentation - getLedgers <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getLedgers>`_

        :param start_ledger: The first ledger to include in the results.
        :param cursor: A cursor value for use in pagination.
        :param limit: The maximum number of records to return.
        :return: A :class:`GetLedgersResponse <stellar_sdk.soroban_rpc.GetLedgersResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        pagination = PaginationOptions(cursor=cursor, limit=limit)
        data = GetLedgersRequest(
            startLedger=start_ledger,
            pagination=pagination,
        )
        request: Request = Request[GetLedgersRequest](
            id=_generate_unique_request_id(), method="getLedgers", params=data
        )
        return self._post(request, GetLedgersResponse)

    def load_account(self, account_id: str) -> Account:
        """Load an account from the server, you can use the returned account
        object as source account for transactions.

        :param account_id: The account ID.
        :return: An :class:`Account <stellar_sdk.account.Account>` object.
        :raises: :exc:`AccountNotFoundException <stellar_sdk.exceptions.AccountNotFoundException>` - If the account is not found on the network.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        account_id_xdr = Keypair.from_public_key(account_id).xdr_account_id()
        key = stellar_xdr.LedgerKey(
            stellar_xdr.LedgerEntryType.ACCOUNT,
            account=stellar_xdr.LedgerKeyAccount(account_id=account_id_xdr),
        )

        resp = self.get_ledger_entries([key])
        if not resp.entries:
            raise AccountNotFoundException(account_id)
        assert len(resp.entries) == 1
        data = stellar_xdr.LedgerEntryData.from_xdr(resp.entries[0].xdr)
        assert data.account is not None
        return Account(account_id, data.account.seq_num.sequence_number.int64)

    def get_contract_data(
        self,
        contract_id: str,
        key: stellar_xdr.SCVal,
        durability: Durability = Durability.PERSISTENT,
    ) -> Optional[LedgerEntryResult]:
        """Reads the current value of contract data ledger entries directly.

        :param contract_id: The contract ID containing the data to load. Encoded as Stellar Contract Address,
            for example: ``"CCJZ5DGASBWQXR5MPFCJXMBI333XE5U3FSJTNQU7RIKE3P5GN2K2WYD5"``
        :param key: The key of the contract data to load.
        :param durability: The "durability keyspace" that this ledger key belongs to, which is either
            :class:`Durability.TEMPORARY` or :class:`Durability.PERSISTENT`. Defaults to :class:`Durability.PERSISTENT`.
        :return: A :class:`LedgerEntryResult <stellar_sdk.soroban_rpc.LedgerEntryResult>` object contains the ledger entry result or ``None`` if not found.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        sc_address = Address(contract_id).to_xdr_sc_address()
        xdr_durability = (
            stellar_xdr.ContractDataDurability.PERSISTENT
            if durability == Durability.PERSISTENT
            else stellar_xdr.ContractDataDurability.TEMPORARY
        )
        contract_key = stellar_xdr.LedgerKey(
            stellar_xdr.LedgerEntryType.CONTRACT_DATA,
            contract_data=stellar_xdr.LedgerKeyContractData(
                contract=sc_address,
                key=key,
                durability=xdr_durability,
            ),
        )
        resp = self.get_ledger_entries([contract_key])
        entries = resp.entries
        if not entries:
            return None
        return entries[0]

    def get_version_info(self) -> GetVersionInfoResponse:
        """Version information about the RPC and Captive core.

        See `Soroban RPC Documentation - getVersionInfo <https://developers.stellar.org/docs/data/rpc/api-reference/methods/getVersionInfo>`_

        :return: A :class:`GetVersionInfoResponse <stellar_sdk.soroban_rpc.GetVersionInfoResponse>` object.
        :raises: :exc:`SorobanRpcErrorResponse <stellar_sdk.exceptions.SorobanRpcErrorResponse>` - If the Soroban-RPC instance returns an error response.
        """
        request: Request = Request(
            id=_generate_unique_request_id(),
            method="getVersionInfo",
            params=None,
        )
        return self._post(request, GetVersionInfoResponse)

    def get_sac_balance(
        self, contract_id: str, sac: Asset, network_passphrase: Optional[str] = None
    ) -> GetSACBalanceResponse:
        """Returns a contract's balance of a particular SAC asset, if any.

        This is a convenience wrapper around :meth:`SorobanServer.get_ledger_entries`.

        :param contract_id: The contract ID whose balance of `sac` you want to know.
        :param sac: The build-in SAC token that you are querying from the given contract.
        :param network_passphrase: The network passphrase to use for the contract ID. If not provided, it will use the
            network passphrase of the current network. We suggest you set it to enhance performance.
        :return: A :class:`GetSACBalanceResponse <stellar_sdk.soroban_rpc.GetSACBalanceResponse>` which will contain the balance entry details if and only if the request returned a valid balance ledger
            entry. If it doesn't, the `balance_entry` field will not exist.
        """
        if not StrKey.is_valid_contract(contract_id):
            raise ValueError(f"Invalid contract ID: {contract_id}")

        if network_passphrase is None:
            network_passphrase = self.get_network().passphrase

        sac_id = sac.contract_id(network_passphrase)
        key = scval.to_vec([scval.to_symbol("Balance"), scval.to_address(sac_id)])
        ledger_key = LedgerKey(
            LedgerEntryType.CONTRACT_DATA,
            contract_data=LedgerKeyContractData(
                contract=Address(sac_id).to_xdr_sc_address(),
                key=key,
                durability=ContractDataDurability.PERSISTENT,
            ),
        )
        response = self.get_ledger_entries([ledger_key])
        if not response.entries:
            return GetSACBalanceResponse(
                latest_ledger=response.latest_ledger, balance_entry=None
            )

        raw_entry = response.entries[0]
        entry_data = LedgerEntryData.from_xdr(raw_entry.xdr)

        if entry_data.type != LedgerEntryType.CONTRACT_DATA:
            return GetSACBalanceResponse(
                latest_ledger=response.latest_ledger, balance_entry=None
            )

        assert entry_data.contract_data is not None
        contract_data = scval.to_native(entry_data.contract_data.val)
        assert isinstance(contract_data, dict)
        return GetSACBalanceResponse(
            latest_ledger=response.latest_ledger,
            balance_entry=SACBalanceEntry(
                amount=contract_data["amount"],
                authorized=contract_data["authorized"],
                clawback=contract_data["clawback"],
                last_modified_ledger=raw_entry.last_modified_ledger,
                live_until_ledger=raw_entry.live_until_ledger,
            ),
        )

    def prepare_transaction(
        self,
        transaction_envelope: TransactionEnvelope,
        simulate_transaction_response: Optional[SimulateTransactionResponse] = None,
    ) -> TransactionEnvelope:
        """Submit a trial contract invocation, first run a simulation of the contract
        invocation as defined on the incoming transaction, and apply the results to
        a new copy of the transaction which is then returned. Setting the ledger
        footprint and authorization, so the resulting transaction is ready for signing
        and sending.

        The returned transaction will also have an updated fee that is the sum of fee
        set on incoming transaction with the contract resource fees estimated from
        simulation. It is advisable to check the fee on returned transaction and validate
        or take appropriate measures for interaction with user to confirm it is acceptable.

        You can call the :meth:`simulate_transaction` method directly first if you
        want to inspect estimated fees for a given transaction in detail first if that is
        of importance.

        :param transaction_envelope: The transaction to prepare. It should include exactly one operation, which
            must be one of :py:class:`RestoreFootprint <stellar_sdk.operation.RestoreFootprint>`,
            :py:class:`ExtendFootprintTTL <stellar_sdk.operation.ExtendFootprintTTL>`,
            or :py:class:`InvokeHostFunction <stellar_sdk.operation.InvokeHostFunction>`. Any provided
            footprint will be ignored. You can use :meth:`stellar_sdk.Transaction.is_soroban_transaction` to check
            if a transaction is a Soroban transaction. Any provided footprint will be overwritten.
            However, if your operation has existing auth entries, they will be preferred over ALL auth
            entries from the simulation. In other words, if you include auth entries, you don't care
            about the auth returned from the simulation. Other fields (footprint, etc.) will be filled
            as normal.
        :param simulate_transaction_response: The response of the simulation of the transaction,
            typically you don't need to pass this parameter, it will be automatically called if you don't pass it.
        :return: A copy of the :class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`,
            with the expected authorizations (in the case of invocation) and ledger footprint added.
            The transaction fee will also automatically be padded with the contract's minimum resource fees
            discovered from the simulation.
        """
        if not simulate_transaction_response:
            simulate_transaction_response = self.simulate_transaction(
                transaction_envelope
            )
        if simulate_transaction_response.error:
            raise PrepareTransactionException(
                "Simulation transaction failed, the response contains error information.",
                simulate_transaction_response,
            )
        te = _assemble_transaction(transaction_envelope, simulate_transaction_response)
        return te

    def close(self) -> None:
        """Close underlying connector, and release all acquired resources."""
        self._client.close()

    def _post(self, request_body: Request, response_body_type: Type[V]) -> V:
        json_data = request_body.model_dump_json(by_alias=True)
        data = self._client.post(
            self.server_url,
            json_data=json.loads(json_data),
        )
        raw_response = Response[Any].model_validate(data.json())

        if raw_response.error:
            raise SorobanRpcErrorResponse(
                raw_response.error.code,
                raw_response.error.message,
                raw_response.error.data,
            )
        assert raw_response.result is not None
        return response_body_type.model_validate(raw_response.result)

    def __enter__(self) -> "SorobanServer":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return f"<SorobanServer [server_url={self.server_url}, client={self._client}]>"
