from typing import Union, TypeVar, AsyncGenerator, Generator

from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..response.orderbook_response import OrderbookResponse
from ..response.wrapped_response import WrappedResponse

T = TypeVar("T")


class OrderbookCallBuilder(BaseCallBuilder[T]):
    """ Creates a new :class:`OrderbookCallBuilder` pointed to server defined by horizon_url.
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

    def _parse_response(self, raw_data: dict) -> Union[OrderbookResponse]:
        return self._base_parse_response(raw_data, OrderbookResponse)

    def stream(
        self,
    ) -> Union[
        AsyncGenerator[WrappedResponse[OrderbookResponse], None],
        Generator[WrappedResponse[OrderbookResponse], None, None],
    ]:
        return self._stream()
