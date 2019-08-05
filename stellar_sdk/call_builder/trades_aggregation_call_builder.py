from typing import Union
from urllib.parse import urljoin

from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..exceptions import ValueError


class TradeAggregationsCallBuilder(BaseCallBuilder):
    def __init__(
        self,
        horizon_url: str,
        client: Union[BaseAsyncClient, BaseSyncClient],
        base: Asset,
        counter: Asset,
        resolution: int,
        start_time: int = None,
        end_time: int = None,
        offset: int = None,
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint = "trade_aggregations"

        if not self.__is_valid_resolution(resolution):
            raise ValueError("Invalid resolution: {}".format(resolution))

        if offset and not self.__is_valid_offset(offset, resolution):
            raise ValueError("Invalid offset: {}".format(offset))

        params = {
            "base_asset_type": base.type,
            "base_asset_code": None if base.is_native() else base.code,
            "base_asset_issuer": base.issuer,
            "counter_asset_type": counter.type,
            "counter_asset_code": None if counter.is_native() else counter.code,
            "counter_asset_issuer": counter.issuer,
            "start_time": start_time,
            "end_time": end_time,
            "resolution": resolution,
            "offset": offset,
        }
        self._add_query_params(params)

    def __is_valid_offset(self, offset: int, resolution: int) -> bool:
        hour = 3600000
        invalid = offset > resolution or offset >= 24 * hour or offset % hour != 0
        return not invalid

    def __is_valid_resolution(self, resolution: int) -> bool:
        allowed_resolutions = (60000, 300000, 900000, 3600000, 86400000, 604800000)
        if resolution in allowed_resolutions:
            return True
