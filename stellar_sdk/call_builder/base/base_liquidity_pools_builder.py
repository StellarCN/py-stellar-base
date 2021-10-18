from typing import List

from ... import Asset
from ...call_builder.base.base_call_builder import BaseCallBuilder
from ...utils import convert_assets_to_horizon_param

__all__ = ["BaseLiquidityPoolsBuilder"]


class BaseLiquidityPoolsBuilder(BaseCallBuilder):
    """Creates a new :class:`LiquidityPoolsBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.liquidity_pools`.

    See `Liquidity Pools <https://developers.stellar.org/api/resources/liquiditypools/>`_

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "liquidity_pools"

    def liquidity_pool(self, liquidity_pool_id: str):
        """Provides information on a liquidity pool.

        See `Retrieve a Liquidity Pool <https://developers.stellar.org/api/resources/liquiditypools/single/>`_

        :param liquidity_pool_id: The ID of the liquidity pool in hex string.
        :return: current LiquidityPoolsBuilder instance
        """
        self.endpoint = f"liquidity_pools/{liquidity_pool_id}"
        return self

    def for_reserves(self, reserves: List[Asset]):
        """Get pools by reserves.

        Horizon will provide an endpoint to find all liquidity pools
        which contain a given set of reserve assets.

        See `List Liquidity Pools <https://developers.stellar.org/api/resources/liquiditypools/list/>`_

        :return: current LiquidityPoolsBuilder instance
        """
        reserves_param = convert_assets_to_horizon_param(reserves)
        self._add_query_param("reserves", reserves_param)
        return self
