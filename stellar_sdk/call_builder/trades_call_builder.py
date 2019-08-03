from typing import Union

from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class TradesCallBuilder(BaseCallBuilder):
    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "trades"

    def for_asset_pair(self, base: Asset, counter: Asset) -> "TradesCallBuilder":
        params = {
            "base_asset_type": base.type,
            "base_asset_code": None if base.is_native() else base.code,
            "base_asset_issuer": base.issuer,
            "counter_asset_type": counter.type,
            "counter_asset_code": None if counter.is_native() else counter.code,
            "counter_asset_issuer": counter.issuer,
        }
        self._add_query_params(params)
        return self

    def for_offer(self, offer_id: Union[int, str]) -> "TradesCallBuilder":
        self._add_query_param("offer_id", offer_id)
        return self

    def for_account(self, account_id: str) -> "TradesCallBuilder":
        self.endpoint = "accounts/{account_id}/trades".format(account_id=account_id)
        return self
