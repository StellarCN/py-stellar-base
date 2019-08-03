from typing import Union

from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class PathsCallBuilder(BaseCallBuilder):
    def __init__(
        self,
        horizon_url: str,
        client: Union[BaseAsyncClient, BaseSyncClient],
        source_account: str,
        destination_account: str,
        destination_asset: Asset,
        destination_amount: str,
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "paths"
        params = {
            "destination_account": destination_account,
            "source_account": source_account,
            "destination_amount": destination_amount,
            "destination_asset_type": destination_asset.type,
            "destination_asset_code": None
            if destination_asset.is_native()
            else destination_asset.code,
            "destination_asset_issuer": destination_asset.issuer,
        }
        self._add_query_params(params)
