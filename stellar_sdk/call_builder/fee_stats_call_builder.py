from typing import Union

from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient

__all__ = ["FeeStatsCallBuilder"]


class FeeStatsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`FeeStatsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.fee_stats`.

    See `Fee Stats <https://www.stellar.org/developers/horizon/reference/endpoints/fee-stats.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "fee_stats"
