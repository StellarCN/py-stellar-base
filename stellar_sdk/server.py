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
from .call_builder.trades_aggregation_call_builder import TradeAggregationsCallBuilder
from .call_builder.trades_call_builder import TradesCallBuilder
from .call_builder.transactions_call_builder import TransactionsCallBuilder
from .client.base_async_client import BaseAsyncClient
from .client.base_sync_client import BaseSyncClient
from .client.requests_client import RequestsClient
from .client.response import Response
from .transaction_envelope import TransactionEnvelope
from .exceptions import ValueError, raise_request_exception

__all__ = ["Server"]


class Server:
    def __init__(
        self,
        horizon_url: str = "https://horizon-testnet.stellar.org/",
        client: Union[BaseAsyncClient, BaseSyncClient] = None,
    ) -> None:
        self.horizon_url: str = horizon_url

        if not client:
            # TODO: warning here
            client = RequestsClient()
        self._client: Union[BaseAsyncClient, BaseSyncClient] = client

        if isinstance(self._client, BaseAsyncClient):
            self.__async: bool = True
        elif isinstance(self._client, BaseSyncClient):
            self.__async = False
        else:
            raise ValueError(
                "This `client` class should be an instance "
                "of `stellar_sdk.client.base_async_client.BaseAsyncClient` "
                "or `stellar_sdk.client.base_sync_client.BaseSyncClient`."
            )

    def submit_transaction(
        self, transaction_envelope: Union[TransactionEnvelope, str]
    ) -> Union[Dict[str, Any], Coroutine[Any, Any, Dict[str, Any]]]:
        xdr = transaction_envelope
        if isinstance(transaction_envelope, TransactionEnvelope):
            xdr = transaction_envelope.to_xdr()

        data = {"tx": xdr}
        url = urljoin(self.horizon_url, "/transactions")
        if self.__async:
            return self.__submit_async(url, data)
        return self.__submit_sync(url, data)

    def __submit_sync(self, url, data):
        resp = self._client.post(url=url, data=data)
        raise_request_exception(resp)
        return resp.json()

    async def __submit_async(self, url, data):
        resp = await self._client.post(url=url, data=data)
        raise_request_exception(resp)
        return resp.json()

    def accounts(self) -> AccountsCallBuilder:
        """
        :return: New :class:`AccountsCallBuilder` object configured by a current Horizon server configuration.
        """
        return AccountsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def assets(self) -> AssetsCallBuilder:
        return AssetsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def effects(self) -> EffectsCallBuilder:
        return EffectsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def fee_stats(self) -> FeeStatsCallBuilder:
        return FeeStatsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def ledgers(self) -> LedgersCallBuilder:
        return LedgersCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def offers(self, account_id: str) -> OffersCallBuilder:
        return OffersCallBuilder(
            horizon_url=self.horizon_url, client=self._client, account_id=account_id
        )

    def operations(self) -> OperationsCallBuilder:
        return OperationsCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def orderbook(self, selling: Asset, buying: Asset) -> OrderbookCallBuilder:
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
        return PathsCallBuilder(
            horizon_url=self.horizon_url,
            client=self._client,
            source_account=source_account,
            destination_account=destination_account,
            destination_asset=destination_asset,
            destination_amount=destination_amount,
        )

    def payments(self) -> PaymentsCallBuilder:
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
        return TradesCallBuilder(horizon_url=self.horizon_url, client=self._client)

    def transactions(self) -> TransactionsCallBuilder:
        return TransactionsCallBuilder(
            horizon_url=self.horizon_url, client=self._client
        )

    def load_account(
        self, account_id: str
    ) -> Union[Account, Coroutine[Any, Any, Account]]:
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

    def close(self):
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
