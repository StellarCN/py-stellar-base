from typing import Union, Coroutine, Any, Dict
from urllib.parse import urljoin

from .account import Account
from .asset import Asset
from .call_builder.accounts_call_builder import AccountsCallBuilder
from .call_builder.assets_call_builder import AssetsCallBuilder
from .call_builder.effects_call_builder import EffectsCallBuilder
from .call_builder.fee_stats_call_builder import FeeStatsCallBuilder
from .call_builder.ledgers_call_builder import LedgersCallBuilder
from .call_builder.offers_call_builder import OffersCallBuilder
from .call_builder.operations_call_builder import OperationsCallBuilder
from .call_builder.orderbook_call_builder import OrderbookCallBuilder
from .call_builder.paths_call_builder import PathsCallBuilder
from .call_builder.payments_call_builder import PaymentsCallBuilder
from .call_builder.root_call_builder import RootCallBuilder
from .call_builder.trades_aggregation_call_builder import TradeAggregationsCallBuilder
from .call_builder.trades_call_builder import TradesCallBuilder
from .call_builder.transactions_call_builder import TransactionsCallBuilder
from .client.base_async_client import BaseAsyncClient
from .client.base_sync_client import BaseSyncClient
from .client.requests_client import RequestsClient
from .exceptions import TypeError, raise_request_exception
from .transaction_envelope import TransactionEnvelope

__all__ = ["Server"]


class Server:
    """Server handles the network connection to a `Horizon <https://www.stellar.org/developers/horizon/reference/>`_
    instance and exposes an interface for requests to that instance.

    Here we need to talk about the **client** parameter, if you do not specify the client, we will use
    the :class:`stellar_sdk.client.requests_client.RequestsClient` instance by default, it is a synchronous HTTPClient,
    you can also specify an asynchronous HTTP Client,
    for example: :class:`stellar_sdk.client.aiohttp_client.AiohttpClient`. If you use a synchronous client,
    then all requests are synchronous. If you use an asynchronous client,
    then all requests are asynchronous. The choice is in your hands.

    :param horizon_url: Horizon Server URL (ex. `https://horizon-testnet.stellar.org`)
    :param client: Http Client used to send the request
    :raises:
        :exc:`ValueError: <stellar_sdk.exceptions.ValueError:>`
    """

    def __init__(
        self,
        horizon_url: str = "https://horizon-testnet.stellar.org/",
        client: Union[BaseAsyncClient, BaseSyncClient] = None,
    ) -> None:
        self.horizon_url: str = horizon_url

        if not client:
            client = RequestsClient()
        self._client: Union[BaseAsyncClient, BaseSyncClient] = client

        if isinstance(self._client, BaseAsyncClient):
            self.__async: bool = True
        elif isinstance(self._client, BaseSyncClient):
            self.__async = False
        else:
            raise TypeError(
                "This `client` class should be an instance "
                "of `stellar_sdk.client.base_async_client.BaseAsyncClient` "
                "or `stellar_sdk.client.base_sync_client.BaseSyncClient`."
            )

    def submit_transaction(
        self, transaction_envelope: Union[TransactionEnvelope, str]
    ) -> Union[Dict[str, Any], Coroutine[Any, Any, Dict[str, Any]]]:
        """Submits a transaction to the network.

        :param transaction_envelope: :class:`stellar_sdk.transaction_envelope.TransactionEnvelope` object
            or base64 encoded xdr
        :return: the response from horizon
        """
        xdr = transaction_envelope
        if isinstance(transaction_envelope, TransactionEnvelope):
            xdr = transaction_envelope.to_xdr()

        data = {"tx": xdr}
        url = urljoin(self.horizon_url, "/transactions")
        if self.__async:
            return self.__submit_transaction_async(url, data)
        return self.__submit_transaction_sync(url, data)

    def __submit_transaction_sync(
        self, url: str, data: Dict[str, str]
    ) -> Dict[str, Any]:
        resp = self._client.post(url=url, data=data)
        raise_request_exception(resp)
        return resp.json()

    async def __submit_transaction_async(
        self, url: str, data: Dict[str, str]
    ) -> Dict[str, Any]:
        resp = await self._client.post(url=url, data=data)
        raise_request_exception(resp)
        return resp.json()

    def root(self) -> RootCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.RootCallBuilder` object configured
            by a current Horizon server configuration.
        """
        return RootCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def accounts(self) -> AccountsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.AccountsCallBuilder` object configured
            by a current Horizon server configuration.
        """
        return AccountsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def assets(self) -> AssetsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.AssetsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return AssetsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def effects(self) -> EffectsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.EffectsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return EffectsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def fee_stats(self) -> FeeStatsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.FeeStatsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return FeeStatsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def ledgers(self) -> LedgersCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.LedgersCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return LedgersCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def offers(self, account_id: str) -> OffersCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.OffersCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return OffersCallBuilder(
            horizon_url=self.horizon_url, client=self._client, account_id=account_id
        )

    def operations(self) -> OperationsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.OperationsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return OperationsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def orderbook(self, selling: Asset, buying: Asset) -> OrderbookCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.OrderbookCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return OrderbookCallBuilder(
            horizon_url=self.horizon_url,
            client=self._client,
            buying=buying,
            selling=selling,
        )

    def paths(
        self,
        source_account: str,
        destination_account: str,
        destination_asset: Asset,
        destination_amount: str,
    ) -> PathsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.PathsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return PathsCallBuilder(
            horizon_url=self.horizon_url,
            client=self._client,
            source_account=source_account,
            destination_account=destination_account,
            destination_asset=destination_asset,
            destination_amount=destination_amount,
        )

    def payments(self) -> PaymentsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.PaymentsCallBuilder` object configured by
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
        :return: New :class:`stellar_sdk.call_builder.TradeAggregationsCallBuilder` object configured by
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
        :return: New :class:`stellar_sdk.call_builder.TradesCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return TradesCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def transactions(self) -> TransactionsCallBuilder:
        """
        :return: New :class:`stellar_sdk.call_builder.TransactionsCallBuilder` object configured by
            a current Horizon server configuration.
        """
        return TransactionsCallBuilder(
            horizon_url=self.horizon_url, client=self._client
        )

    def load_account(
        self, account_id: str
    ) -> Union[Account, Coroutine[Any, Any, Account]]:
        """Fetches an account's most current state in the ledger and then creates
        and returns an :class:`stellar_sdk.account.Account` object.

        :param account_id: The account to load.
        :return: an :class:`stellar_sdk.account.Account` object.
        :raises:
            :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
            :exc:`NotFoundError <stellar_sdk.exceptions.NotFoundError>`
            :exc:`BadRequestError <stellar_sdk.exceptions.BadRequestError>`
            :exc:`BadResponseError <stellar_sdk.exceptions.BadResponseError>`
            :exc:`UnknownRequestError <stellar_sdk.exceptions.UnknownRequestError>`
        """
        if self.__async:
            return self.__load_account_async(account_id)
        return self.__load_account_sync(account_id)

    async def __load_account_async(self, account_id: str) -> Account:
        resp = await self.accounts().account_id(account_id=account_id).call()
        sequence = int(resp["sequence"])
        return Account(account_id=account_id, sequence=sequence)

    def __load_account_sync(self, account_id: str) -> Account:
        resp = self.accounts().account_id(account_id=account_id).call()
        sequence = int(resp["sequence"])
        return Account(account_id=account_id, sequence=sequence)

    def fetch_base_fee(self) -> Union[int, Coroutine[Any, Any, int]]:
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
        if self.__async:
            return self.__fetch_base_fee_async()
        return self.__fetch_base_fee_sync()

    def __fetch_base_fee_sync(self) -> int:
        latest_ledger = self.ledgers().order(desc=True).limit(1).call()
        base_fee = self.__handle_base_fee(latest_ledger)
        return base_fee

    async def __fetch_base_fee_async(self) -> int:
        latest_ledger = await self.ledgers().order(desc=True).limit(1).call()
        base_fee = self.__handle_base_fee(latest_ledger)
        return base_fee

    def __handle_base_fee(self, latest_ledger: dict) -> int:
        base_fee = 100
        if (
            latest_ledger["_embedded"]
            and latest_ledger["_embedded"]["records"]
            and latest_ledger["_embedded"]["records"][0]
        ):
            base_fee = int(
                latest_ledger["_embedded"]["records"][0]["base_fee_in_stroops"]
            )
        return base_fee

    def close(self) -> Union[None, Coroutine[Any, Any, None]]:
        """Close underlying connector.

        Release all acquired resources.
        """
        if self.__async:
            return self.__close_async()
        else:
            return self.__close_sync()

    async def __close_async(self) -> None:
        await self._client.close()

    def __close_sync(self) -> None:
        self._client.close()

    async def __aenter__(self) -> "Server":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    def __enter__(self) -> "Server":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
