from ...call_builder.base import BaseOffersCallBuilder
from ...call_builder.call_builder_async.base_call_builder import BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient

__all__ = ["OffersCallBuilder"]


class OffersCallBuilder(BaseCallBuilder, BaseOffersCallBuilder):
    """Creates a new :class:`OffersCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.ServerAsync.offers`.

    See `List All Offers <https://developers.stellar.org/api/resources/offers/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseAsyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
