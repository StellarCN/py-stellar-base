from decimal import Decimal
from typing import Any, Dict, List, Union

from .account import Account
from .asset import Asset
from .base_server import BaseServer
from .call_builder.call_builder_sync import *
from .client.base_sync_client import BaseSyncClient
from .client.requests_client import RequestsClient
from .client.response import Response
from .exceptions import NotFoundError, raise_request_exception
from .fee_bump_transaction import FeeBumpTransaction
from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from .keypair import Keypair
from .memo import NoneMemo
from .muxed_account import MuxedAccount
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope
from .utils import MUXED_ACCOUNT_STARTING_LETTER, urljoin_with_query

__all__ = ["Server"]


class Server(BaseServer):
    """Server handles the network connection to a `Horizon <https://developers.stellar.org/api/introduction/>`_
    instance and exposes an interface for requests to that instance.

    An example::

        from stellar_sdk import Server

        server = Server("https://horizon-testnet.stellar.org")
        resp = server.transactions().limit(10).order(desc=True).call()
        print(resp)

    :param horizon_url: Horizon Server URL
        (ex. ``"https://horizon-testnet.stellar.org"`` for test network,
        ``"https://horizon.stellar.org"`` for public network)
    :param client: Http client used to send the request
    """

    def __init__(
        self,
        horizon_url: str = "https://horizon-testnet.stellar.org/",
        client: BaseSyncClient = None,
    ) -> None:
        self.horizon_url: str = horizon_url

        if not client:
            client = RequestsClient()
        self._client: BaseSyncClient = client

    def submit_transaction(
        self,
        transaction_envelope: Union[
            TransactionEnvelope, FeeBumpTransactionEnvelope, str
        ],
        skip_memo_required_check: bool = False,
    ) -> Dict[str, Any]:
        """Submits a transaction to the network.

        :param transaction_envelope: :class:`stellar_sdk.transaction_envelope.TransactionEnvelope` object
            or base64 encoded xdr
        :param skip_memo_required_check: Allow skipping memo
        :return: the response from horizon
        :raises:
            :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
            :exc:`NotFoundError <stellar_sdk.exceptions.NotFoundError>`
            :exc:`BadRequestError <stellar_sdk.exceptions.BadRequestError>`
            :exc:`BadResponseError <stellar_sdk.exceptions.BadResponseError>`
            :exc:`UnknownRequestError <stellar_sdk.exceptions.UnknownRequestError>`
            :exc:`AccountRequiresMemoError <stellar_sdk.sep.exceptions.AccountRequiresMemoError>`
        """
        url = urljoin_with_query(self.horizon_url, "transactions")
        xdr, tx = self._get_xdr_and_transaction_from_transaction_envelope(
            transaction_envelope
        )
        if not skip_memo_required_check:
            self.__check_memo_required_sync(tx)
        data = {"tx": xdr}
        resp = self._client.post(url=url, data=data)
        assert isinstance(resp, Response)
        raise_request_exception(resp)
        return resp.json()

    def submit_transaction_async(
        self,
        transaction_envelope: Union[
            TransactionEnvelope, FeeBumpTransactionEnvelope, str
        ],
        skip_memo_required_check: bool = False,
    ) -> Dict[str, Any]:
        """Submits an asynchronous transaction to the network. Unlike the synchronous version, which blocks
        and waits for the transaction to be ingested in Horizon, this endpoint relays the response from
        core directly back to the user.

        See `Horizon Documentation - Submit a Transaction Asynchronously <https://developers.stellar.org/docs/data/horizon/api-reference/resources/submit-async-transaction>`_

        :param transaction_envelope: :class:`stellar_sdk.transaction_envelope.TransactionEnvelope` object
            or base64 encoded xdr
        :param skip_memo_required_check: Allow skipping memo
        :return: the response from horizon
        :raises:
            :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
            :exc:`NotFoundError <stellar_sdk.exceptions.NotFoundError>`
            :exc:`BadRequestError <stellar_sdk.exceptions.BadRequestError>`
            :exc:`BadResponseError <stellar_sdk.exceptions.BadResponseError>`
            :exc:`UnknownRequestError <stellar_sdk.exceptions.UnknownRequestError>`
            :exc:`AccountRequiresMemoError <stellar_sdk.sep.exceptions.AccountRequiresMemoError>`
        """
        url = urljoin_with_query(self.horizon_url, "transactions_async")
        xdr, tx = self._get_xdr_and_transaction_from_transaction_envelope(
            transaction_envelope
        )
        if not skip_memo_required_check:
            self.__check_memo_required_sync(tx)
        data = {"tx": xdr}
        resp = self._client.post(url=url, data=data)
        assert isinstance(resp, Response)
        raise_request_exception(resp)
        return resp.json()

    def load_account(self, account_id: Union[MuxedAccount, Keypair, str]) -> Account:
        """Fetches an account's most current base state (like sequence) in the ledger and then creates
        and returns an :class:`stellar_sdk.account.Account` object.

        If you want to get complete account information, please
        use :func:`stellar_sdk.server.Server.accounts`.

        :param account_id: The account to load.
        :return: an :class:`stellar_sdk.account.Account` object.
        :raises:
            :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
            :exc:`NotFoundError <stellar_sdk.exceptions.NotFoundError>`
            :exc:`BadRequestError <stellar_sdk.exceptions.BadRequestError>`
            :exc:`BadResponseError <stellar_sdk.exceptions.BadResponseError>`
            :exc:`UnknownRequestError <stellar_sdk.exceptions.UnknownRequestError>`
        """
        if isinstance(account_id, str):
            account_id = MuxedAccount.from_account(account_id)
        elif isinstance(account_id, Keypair):
            account_id = MuxedAccount.from_account(account_id.public_key)
        else:
            account_id = account_id
        resp = self.accounts().account_id(account_id=account_id.account_id).call()
        sequence = int(resp["sequence"])
        account = Account(account=account_id, sequence=sequence, raw_data=resp)
        return account

    def __check_memo_required_sync(
        self, transaction: Union[Transaction, FeeBumpTransaction]
    ) -> None:
        if isinstance(transaction, FeeBumpTransaction):
            transaction = transaction.inner_transaction_envelope.transaction
        if not (transaction.memo is None or isinstance(transaction.memo, NoneMemo)):
            return
        for index, destination in self._get_check_memo_required_destinations(
            transaction
        ):
            if destination.startswith(MUXED_ACCOUNT_STARTING_LETTER):
                continue
            try:
                account_resp = self.accounts().account_id(destination).call()
            except NotFoundError:
                continue
            assert isinstance(account_resp, dict)
            self._check_destination_memo(account_resp, index, destination)

    def fetch_base_fee(self) -> int:
        """Fetch the base fee. Since this hits the server, if the server call fails,
        you might get an error. You should be prepared to use a default value if that happens.

        :return: the base fee
        :raises:
            :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
            :exc:`NotFoundError <stellar_sdk.exceptions.NotFoundError>`
            :exc:`BadRequestError <stellar_sdk.exceptions.BadRequestError>`
            :exc:`BadResponseError <stellar_sdk.exceptions.BadResponseError>`
            :exc:`UnknownRequestError <stellar_sdk.exceptions.UnknownRequestError>`
        """
        latest_ledger = self.ledgers().order(desc=True).limit(1).call()
        assert isinstance(latest_ledger, dict)
        base_fee = self._handle_base_fee(latest_ledger)
        return base_fee

    def root(self) -> RootCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.RootCallBuilder` object configured
            by a current Horizon server configuration.
        """
        return RootCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def accounts(self) -> AccountsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.AccountsCallBuilder` object configured
            by a current Horizon server configuration.
        """
        return AccountsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def assets(self) -> AssetsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.AssetsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return AssetsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def claimable_balances(self) -> ClaimableBalancesCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.ClaimableBalancesCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return ClaimableBalancesCallBuilder(
            horizon_url=self.horizon_url, client=self._client
        )

    def data(self, account_id: str, data_name: str) -> DataCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.DataCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return DataCallBuilder(
            horizon_url=self.horizon_url,
            client=self._client,
            account_id=account_id,
            data_name=data_name,
        )

    def effects(self) -> EffectsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.EffectsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return EffectsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def fee_stats(self) -> FeeStatsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.FeeStatsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return FeeStatsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def ledgers(self) -> LedgersCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.LedgersCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return LedgersCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def liquidity_pools(self) -> LiquidityPoolsBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.LiquidityPoolsBuilder` object configured by
            a current Horizon server configuration.
        """
        return LiquidityPoolsBuilder(horizon_url=self.horizon_url, client=self._client)

    def offers(self) -> OffersCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.OffersCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return OffersCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def operations(self) -> OperationsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.OperationsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return OperationsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def orderbook(self, selling: Asset, buying: Asset) -> OrderbookCallBuilder:
        """
        :param selling: Asset being sold
        :param buying: Asset being bought
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.OrderbookCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return OrderbookCallBuilder(
            horizon_url=self.horizon_url,
            client=self._client,
            buying=buying,
            selling=selling,
        )

    def strict_receive_paths(
        self,
        source: Union[str, List[Asset]],
        destination_asset: Asset,
        destination_amount: Union[str, Decimal],
    ) -> StrictReceivePathsCallBuilder:
        """
        :param source: The sender's account ID or a list of Assets. Any returned path must use a source that the sender can hold.
        :param destination_asset: The destination asset.
        :param destination_amount: The amount, denominated in the destination asset, that any returned path should be able to satisfy.
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.StrictReceivePathsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return StrictReceivePathsCallBuilder(
            horizon_url=self.horizon_url,
            client=self._client,
            source=source,
            destination_asset=destination_asset,
            destination_amount=destination_amount,
        )

    def strict_send_paths(
        self,
        source_asset: Asset,
        source_amount: Union[str, Decimal],
        destination: Union[str, List[Asset]],
    ) -> StrictSendPathsCallBuilder:
        """
        :param source_asset: The asset to be sent.
        :param source_amount: The amount, denominated in the source asset, that any returned path should be able to satisfy.
        :param destination: The destination account or the destination assets.
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.StrictReceivePathsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return StrictSendPathsCallBuilder(
            horizon_url=self.horizon_url,
            client=self._client,
            source_asset=source_asset,
            source_amount=source_amount,
            destination=destination,
        )

    def payments(self) -> PaymentsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.PaymentsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return PaymentsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def trade_aggregations(
        self,
        base: Asset,
        counter: Asset,
        resolution: int,
        start_time: int = None,
        end_time: int = None,
        offset: int = None,
    ) -> TradeAggregationsCallBuilder:
        """
        :param base: base asset
        :param counter: counter asset
        :param resolution: segment duration as millis since epoch. *Supported values
            are 1 minute (60000), 5 minutes (300000), 15 minutes (900000),
            1 hour (3600000), 1 day (86400000) and 1 week (604800000).*
        :param start_time: lower time boundary represented as millis since epoch
        :param end_time: upper time boundary represented as millis since epoch
        :param offset: segments can be offset using this parameter.
            Expressed in milliseconds. *Can only be used if the resolution is greater than 1 hour.
            Value must be in whole hours, less than the provided resolution, and less than 24 hours.*
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.TradeAggregationsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return TradeAggregationsCallBuilder(
            horizon_url=self.horizon_url,
            client=self._client,
            base=base,
            counter=counter,
            start_time=start_time,
            end_time=end_time,
            resolution=resolution,
            offset=offset,
        )

    def trades(self) -> TradesCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.TradesCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return TradesCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def transactions(self) -> TransactionsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.call_builder_sync.TransactionsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return TransactionsCallBuilder(
            horizon_url=self.horizon_url, client=self._client
        )

    def close(self) -> None:
        """Close underlying connector, and release all acquired resources."""
        self._client.close()

    def __enter__(self) -> "Server":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return f"<Server [horizon_url={self.horizon_url}, client={self._client}]>"
