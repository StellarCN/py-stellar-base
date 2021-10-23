from ...asset import Asset
from ...call_builder.base import BaseTradeAggregationsCallBuilder
from ...call_builder.call_builder_async.base_call_builder import BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient
from ...type_checked import type_checked

__all__ = ["TradeAggregationsCallBuilder"]


@type_checked
class TradeAggregationsCallBuilder(BaseCallBuilder, BaseTradeAggregationsCallBuilder):
    """Creates a new :class:`TradeAggregationsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.ServerAsync.trade_aggregations`.

    Trade Aggregations facilitate efficient gathering of historical trade data.

    See `List Trade Aggregations <https://developers.stellar.org/api/aggregations/trade-aggregations/list/>`__ for more information.

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
        client: BaseAsyncClient,
        base: Asset,
        counter: Asset,
        resolution: int,
        start_time: int = None,
        end_time: int = None,
        offset: int = None,
    ) -> None:
        super().__init__(
            horizon_url=horizon_url,
            client=client,
            base=base,
            counter=counter,
            resolution=resolution,
            start_time=start_time,
            end_time=end_time,
            offset=offset,
        )
