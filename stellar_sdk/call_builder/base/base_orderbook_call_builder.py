from ...asset import Asset
from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseOrderbookCallBuilder"]


class BaseOrderbookCallBuilder(BaseCallBuilder):
    """Creates a new :class:`OrderbookCallBuilder` pointed to server defined by horizon_url.

    See `Orderbook Details <https://www.stellar.org/developers/horizon/reference/endpoints/orderbook-details.html>`__

    :param selling: Asset being sold
    :param buying: Asset being bought
    :param horizon_url: Horizon server URL.
    """

    def __init__(self, selling: Asset, buying: Asset, **kwargs) -> None:
        super().__init__(**kwargs)
        self.endpoint: str = "order_book"
        params = {
            "selling_asset_type": selling.type,
            "selling_asset_code": None if selling.is_native() else selling.code,
            "selling_asset_issuer": selling.issuer,
            "buying_asset_type": buying.type,
            "buying_asset_code": None if buying.is_native() else buying.code,
            "buying_asset_issuer": buying.issuer,
        }
        self._add_query_params(params)
