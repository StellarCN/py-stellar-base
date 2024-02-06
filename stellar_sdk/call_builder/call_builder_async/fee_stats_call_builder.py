from ...call_builder.base import BaseFeeStatsCallBuilder
from ...call_builder.call_builder_async.base_call_builder import BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient

__all__ = ["FeeStatsCallBuilder"]


class FeeStatsCallBuilder(BaseCallBuilder, BaseFeeStatsCallBuilder):
    """Creates a new :class:`FeeStatsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.ServerAsync.fee_stats`.

    See `Fee Stats <https://developers.stellar.org/api/aggregations/fee-stats/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseAsyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)

    async def stream(
        self,
    ):
        """This endpoint does not support streaming."""
        raise NotImplementedError("Streaming is not supported.")
