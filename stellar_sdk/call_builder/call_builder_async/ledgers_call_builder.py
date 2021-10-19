from ...call_builder.base import BaseLedgersCallBuilder
from ...call_builder.call_builder_async.base_call_builder import BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient

__all__ = ["LedgersCallBuilder"]


class LedgersCallBuilder(BaseCallBuilder, BaseLedgersCallBuilder):
    """Creates a new :class:`LedgersCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.ServerAsync.ledgers`.

    See `All Ledgers <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-all.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseAsyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)
