from typing import Union

from ...asset import Asset
from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseTradesCallBuilder"]


class BaseTradesCallBuilder(BaseCallBuilder):
    """Creates a new :class:`TradesCallBuilder` pointed to server defined by horizon_url.

    See `List All Trades <https://developers.stellar.org/api/resources/trades/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "trades"

    def for_asset_pair(self, base: Asset, counter: Asset):
        """Filter trades for a specific asset pair (orderbook)

        See `List All Trades <https://developers.stellar.org/api/resources/trades/list/>`__ for more information.

        :param base: base asset
        :param counter: counter asset
        :return: current TradesCallBuilder instance
        """
        params = {
            "base_asset_type": base.type,
            "base_asset_code": None if base.is_native() else base.code,
            "base_asset_issuer": base.issuer,
            "counter_asset_type": counter.type,
            "counter_asset_code": None if counter.is_native() else counter.code,
            "counter_asset_issuer": counter.issuer,
        }
        self._add_query_params(params)
        return self

    def for_offer(self, offer_id: Union[int, str]):
        """Filter trades for a specific offer

        See `List All Trades <https://developers.stellar.org/api/resources/trades/list/>`__ for more information.

        :param offer_id: offer id
        :return: current TradesCallBuilder instance
        """
        self.endpoint = f"offers/{offer_id}/trades"
        return self

    def for_account(self, account_id: str):
        """Filter trades for a specific account

        See `Retrieve an Account's Trades <https://developers.stellar.org/api/resources/accounts/trades/>`__ for more information.

        :param account_id: account id
        :return: current TradesCallBuilder instance
        """
        self.endpoint = f"accounts/{account_id}/trades"
        return self

    def for_trade_type(self, trade_type: str):
        """Filter trades for a specific trade type

        Horizon will reject requests which attempt to set
        `trade_type` to ``liquidity_pools`` when using the offer id filter.

        :param trade_type: trade type, the currently supported types are ``"orderbook"``, ``"liquidity_pool"`` and ``"all"``,
            defaults to ``"all"``.
        :return: current TradesCallBuilder instance
        """
        params = {"trade_type": trade_type}
        self._add_query_params(params)
        return self

    def for_liquidity_pool(self, liquidity_pool_id: str):
        """Filter trades for a specific liquidity pool.

        See `Liquidity Pools - Retrieve related Trades <https://developers.stellar.org/api/resources/liquiditypools/trades/>`__

        :param liquidity_pool_id: The ID of the liquidity pool in hex string.
        :return: current TradesCallBuilder instance
        """
        self.endpoint = f"liquidity_pools/{liquidity_pool_id}/trades"
        return self
