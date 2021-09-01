from typing import Union, List

from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..utils import convert_assets_to_horizon_param

__all__ = ["LiquidityPoolsBuilder"]


class LiquidityPoolsBuilder(BaseCallBuilder):
    """Creates a new :class:`LiquidityPoolsBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.ledgers`.

    TODO: docs link

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "liquidity_pools"

    def liquidity_pool(self, liquidity_pool_id: str) -> "LiquidityPoolsBuilder":
        """Provides information on a liquidity pool.

        :param liquidity_pool_id: The ID of the liquidity pool in hex string.
        :return: current LedgerCallBuilder instance
        """
        self.endpoint = f"liquidity_pools/{liquidity_pool_id}"
        return self

    def for_reserves(self, reserves: List[Asset]) -> "LiquidityPoolsBuilder":
        """Get pools by reserves.

        Horizon will provide an endpoint to find all liquidity pools
        which contain a given set of reserve assets.

        """
        reserves_param = convert_assets_to_horizon_param(reserves)
        self._add_query_param("reserves", reserves_param)
        return self
