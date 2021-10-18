from ...asset import Asset
from ...call_builder.base import BaseOrderbookCallBuilder
from ...call_builder.call_builder_async.base_call_builder_async import (
    BaseCallBuilderAsync,
)
from ...client.base_async_client import BaseAsyncClient

__all__ = ["OrderbookCallBuilder"]


class OrderbookCallBuilder(BaseCallBuilderAsync, BaseOrderbookCallBuilder):
    """Creates a new :class:`OrderbookCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.orderbook`.

    See `Orderbook Details <https://www.stellar.org/developers/horizon/reference/endpoints/orderbook-details.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    :param selling: Asset being sold
    :param buying: Asset being bought
    """

    def __init__(
        self,
        horizon_url: str,
        client: BaseAsyncClient,
        selling: Asset,
        buying: Asset,
    ) -> None:
        super().__init__(
            horizon_url=horizon_url, client=client, selling=selling, buying=buying
        )