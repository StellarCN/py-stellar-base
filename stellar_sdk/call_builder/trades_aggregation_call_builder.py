from typing import Union

from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..exceptions import ValueError


class TradeAggregationsCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`TradeAggregationsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.trade_aggregations`.

    Trade Aggregations facilitate efficient gathering of historical trade data.

    See `Trade Aggregations <https://www.stellar.org/developers/horizon/reference/endpoints/trade_aggregations.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
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
    """

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
        self.endpoint: str = "trade_aggregations"

        if not self.__is_valid_resolution(resolution):
            raise ValueError(f"Invalid resolution: {resolution}")

        if offset and not self.__is_valid_offset(offset, resolution):
            raise ValueError(f"Invalid offset: {offset}")

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
        """
        :param offset: Time offset in milliseconds
        :param resolution: Trade data resolution in milliseconds
        :return: `True` if the offset is allowed
        """
        hour = 3600000
        invalid = offset > resolution or offset >= 24 * hour or offset % hour != 0
        return not invalid

    def __is_valid_resolution(self, resolution: int) -> bool:
        """
        :param resolution: Trade data resolution in milliseconds
        :return: `True` if the resolution is allowed
        """
        allowed_resolutions = (60000, 300000, 900000, 3600000, 86400000, 604800000)
        if resolution in allowed_resolutions:
            return True
        return False
