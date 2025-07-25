from typing import Any, Dict, Generator

from ...call_builder.base import BaseTradesCallBuilder
from ...call_builder.call_builder_sync.base_call_builder import BaseCallBuilder
from ...client.base_sync_client import BaseSyncClient

__all__ = ["TradesCallBuilder"]


class TradesCallBuilder(BaseCallBuilder, BaseTradesCallBuilder):
    """Creates a new :class:`TradesCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.Server.trades`.

    See `List All Trades <https://developers.stellar.org/api/resources/trades/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseSyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)

    def stream(
        self,
    ) -> Generator[Dict[str, Any], None, None]:
        """Creates an EventSource that listens for events from the `Trades` endpoint.

        See `Streaming <https://developers.stellar.org/docs/data/apis/horizon/api-reference/structure/streaming>`__ for more information.
        """
        return self._stream()
