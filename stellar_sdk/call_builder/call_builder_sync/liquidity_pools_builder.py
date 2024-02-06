from ...call_builder.base import BaseLiquidityPoolsBuilder
from ...call_builder.call_builder_sync.base_call_builder import BaseCallBuilder
from ...client.base_sync_client import BaseSyncClient

__all__ = ["LiquidityPoolsBuilder"]


class LiquidityPoolsBuilder(BaseCallBuilder, BaseLiquidityPoolsBuilder):
    """Creates a new :class:`LiquidityPoolsBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.Server.liquidity_pools`.

    See `List Liquidity Pools <https://developers.stellar.org/api/resources/liquiditypools/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, horizon_url: str, client: BaseSyncClient) -> None:
        super().__init__(horizon_url=horizon_url, client=client)

    def stream(
        self,
    ):
        """This endpoint does not support streaming."""
        raise NotImplementedError("Streaming is not supported.")
