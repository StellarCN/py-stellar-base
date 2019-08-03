from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class AssetsCallBuilder(BaseCallBuilder):
    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "assets"

    def for_code(self, asset_code: str) -> "AssetsCallBuilder":
        self._add_query_param("asset_code", asset_code)
        return self

    def for_issuer(self, asset_issuer: str) -> "AssetsCallBuilder":
        self._add_query_param("asset_issuer", asset_issuer)
        return self
