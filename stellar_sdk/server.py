from stellar_sdk.account import Account
from stellar_sdk.client.base_sync_client import BaseSyncClient
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
from .client.aiohttp_client import AiohttpClient
from .client.base_async_client import BaseAsyncClient


class Server:
    def __init__(self, horizon_url="https://horizon.stellar.org", client=None):
        self.horizon_url = horizon_url
        self.client = AiohttpClient()
        if isinstance(self.client, BaseAsyncClient):
            self.load_account = self.__load_account_async
        elif isinstance(self.client, BaseSyncClient):
            self.load_account = self.__load_account_sync
        else:
            raise  # TODO

        if client:
            self.client = client

    async def __load_account_async(self, account_id):
        resp = await self.accounts().account_id(account_id=account_id).call()
        sequence = resp.json()['sequence']
        return Account(account_id=account_id, sequence=sequence)

    def __load_account_sync(self, account_id):
        resp = self.accounts().account_id(account_id=account_id).call()
        sequence = resp.json()['sequence']
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

    def paths(self,
              source_account: str,
              destination_account: str,
              destination_asset: Asset,
              destination_amount: str) -> PathsCallBuilder:
        return PathsCallBuilder(horizon_url=self.horizon_url,
                                client=self.client,
                                source_account=source_account,
                                destination_account=destination_account,
                                destination_asset=destination_asset,
                                destination_amount=destination_amount)

    def orderbook(self, buying: Asset, selling: Asset):
        return OrderbookCallBuilder(horizon_url=self.horizon_url,
                                    client=self.client,
                                    buying=buying,
                                    selling=selling)

    def trade_aggregations(self,
                           base: Asset,
                           counter: Asset,
                           start_time: int,
                           end_time: int,
                           resolution: int,
                           offset: int) -> TradeAggregationsCallBuilder:
        return TradeAggregationsCallBuilder(horizon_url=self.horizon_url,
                                            client=self.client,
                                            base=base,
                                            counter=counter,
                                            start_time=start_time,
                                            end_time=end_time,
                                            resolution=resolution,
                                            offset=offset)

    async def __aenter__(self) -> 'Server':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self.client.close()
