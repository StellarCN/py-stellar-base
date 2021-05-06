from typing import Union

from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient

__all__ = ["OrderbookCallBuilder"]


class OrderbookCallBuilder(BaseCallBuilder):
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
        client: Union[BaseAsyncClient, BaseSyncClient],
        selling: Asset,
        buying: Asset,
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "order_book"
        params = {
            "selling_asset_type": selling.type,
            "selling_asset_code": None if selling.is_native() else selling.code,
            "selling_asset_issuer": selling.issuer,
            "buying_asset_type": buying.type,
            "buying_asset_code": None if buying.is_native() else buying.code,
            "buying_asset_issuer": buying.issuer,
        }
        self._add_query_params(params)
