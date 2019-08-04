from typing import Union, Coroutine, Any
from urllib.parse import urljoin

from .account import Account
from .asset import Asset
from .call_builder.accounts_call_builder import AccountsCallBuilder
from .call_builder.assets_call_builder import AssetsCallBuilder
from .call_builder.effects_call_builder import EffectsCallBuilder
from .call_builder.ledgers_call_builder import LedgersCallBuilder
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

__all__ = ["Server"]


class Server:
    def __init__(
        self,
        horizon_url: str = "https://horizon-testnet.stellar.org/",
        client: Union[BaseAsyncClient, BaseSyncClient] = None,
    ) -> None:
        self.horizon_url = horizon_url

        self.client = client
        if not client:
            # TODO: warning here
            self.client = RequestsClient()

        if isinstance(self.client, BaseAsyncClient):
            self.__async: bool = True
        elif isinstance(self.client, BaseSyncClient):
            self.__async: bool = False
        else:
            raise  # TODO

    async def submit_transaction(
        self, transaction_envelope: TransactionEnvelope
    ) -> Response:
        xdr = transaction_envelope
        if isinstance(transaction_envelope, TransactionEnvelope):
            xdr = transaction_envelope.to_xdr()

        params = {"tx": xdr}
        url = urljoin(self.horizon_url, "/transactions")
        return await self.client.post(url=url, params=params)

    def load_account(
        self, account_id: str
    ) -> Union[Account, Coroutine[Any, Any, Account]]:
        if self.__async:
            return self.__load_account_async(account_id)
        return self.__load_account_sync(account_id)

    async def __load_account_async(self, account_id: str) -> Account:
        resp = await self.accounts().account_id(account_id=account_id).call()
        sequence = int(resp.json()["sequence"])
        return Account(account_id=account_id, sequence=sequence)

    def __load_account_sync(self, account_id: str) -> Account:
        resp = self.accounts().account_id(account_id=account_id).call()
        sequence = int(resp.json()["sequence"])
        return Account(account_id=account_id, sequence=sequence)

    def accounts(self) -> AccountsCallBuilder:
        return AccountsCallBuilder(horizon_url=self.horizon_url, client=self.client)

    def assets(self) -> AssetsCallBuilder:
        return AssetsCallBuilder(horizon_url=self.horizon_url, client=self.client)

    def effects(self) -> EffectsCallBuilder:
        return EffectsCallBuilder(horizon_url=self.horizon_url, client=self.client)

    def ledgers(self) -> LedgersCallBuilder:
        return LedgersCallBuilder(horizon_url=self.horizon_url, client=self.client)

    def operations(self) -> OperationsCallBuilder:
        return OperationsCallBuilder(horizon_url=self.horizon_url, client=self.client)

    def payments(self) -> PaymentsCallBuilder:
        return PaymentsCallBuilder(horizon_url=self.horizon_url, client=self.client)

    def trades(self) -> TradesCallBuilder:
        return TradesCallBuilder(horizon_url=self.horizon_url, client=self.client)

    def transactions(self) -> TransactionsCallBuilder:
        return TransactionsCallBuilder(horizon_url=self.horizon_url, client=self.client)

    def paths(
        self,
        source_account: str,
        destination_account: str,
        destination_asset: Asset,
        destination_amount: str,
    ) -> PathsCallBuilder:
        return PathsCallBuilder(
            horizon_url=self.horizon_url,
            client=self.client,
            source_account=source_account,
            destination_account=destination_account,
            destination_asset=destination_asset,
            destination_amount=destination_amount,
        )

    def orderbook(self, buying: Asset, selling: Asset) -> OrderbookCallBuilder:
        return OrderbookCallBuilder(
            horizon_url=self.horizon_url,
            client=self.client,
            buying=buying,
            selling=selling,
        )

    def trade_aggregations(
        self,
        base: Asset,
        counter: Asset,
        start_time: int,
        end_time: int,
        resolution: int,
        offset: int,
    ) -> TradeAggregationsCallBuilder:
        return TradeAggregationsCallBuilder(
            horizon_url=self.horizon_url,
            client=self.client,
            base=base,
            counter=counter,
            start_time=start_time,
            end_time=end_time,
            resolution=resolution,
            offset=offset,
        )

    async def __aenter__(self) -> "Server":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self.client.close()
