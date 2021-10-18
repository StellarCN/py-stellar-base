from ...asset import Asset
from ...call_builder.base import BaseOrderbookCallBuilder
from ...call_builder.call_builder_sync.base_call_builder_sync import BaseCallBuilderSync
from ...client.base_sync_client import BaseSyncClient

__all__ = ["OrderbookCallBuilder"]


class OrderbookCallBuilder(BaseCallBuilderSync, BaseOrderbookCallBuilder):
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
        client: BaseSyncClient,
        selling: Asset,
        buying: Asset,
    ) -> None:
        super().__init__(horizon_url, client)
