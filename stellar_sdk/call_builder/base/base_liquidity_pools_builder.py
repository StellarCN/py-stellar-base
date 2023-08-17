from typing import Sequence

from ...asset import Asset
from ...call_builder.base.base_call_builder import BaseCallBuilder
from ...utils import convert_assets_to_horizon_param

__all__ = ["BaseLiquidityPoolsBuilder"]


class BaseLiquidityPoolsBuilder(BaseCallBuilder):
    """Creates a new :class:`LiquidityPoolsBuilder` pointed to server defined by horizon_url.

    See `List Liquidity Pools <https://developers.stellar.org/api/resources/liquiditypools/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "liquidity_pools"

    def liquidity_pool(self, liquidity_pool_id: str):
        """Provides information on a liquidity pool.

        See `Retrieve a Liquidity Pool <https://developers.stellar.org/api/resources/liquiditypools/single/>`__ for more information.

        :param liquidity_pool_id: The ID of the liquidity pool in hex string.
        :return: current LiquidityPoolsBuilder instance
        """
        self.endpoint = f"liquidity_pools/{liquidity_pool_id}"
        return self

    def for_reserves(self, reserves: Sequence[Asset]):
        """Get pools by reserves.

        Horizon will provide an endpoint to find all liquidity pools
        which contain a given set of reserve assets.

        See `List Liquidity Pools <https://developers.stellar.org/api/resources/liquiditypools/list/>`__ for more information.

        :return: current LiquidityPoolsBuilder instance
        """
        reserves_param = convert_assets_to_horizon_param(reserves)
        self._add_query_param("reserves", reserves_param)
        return self

    def for_account(self, account_id: str):
        """Filter pools for a specific account

        See `List Liquidity Pools <https://developers.stellar.org/api/resources/liquiditypools/list/>`__ for more information.

        :param account_id: account id
        :return: current LiquidityPoolsBuilder instance
        """
        self._add_query_param("account", account_id)
        return self
