from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder


class OrderbookCallBuilder(BaseCallBuilder):
    def __init__(self, horizon_url, client, selling: Asset, buying: Asset):
        super().__init__(horizon_url, client)
        params = {
            'selling_asset_type': selling.type,
            'selling_asset_code': None if selling.is_native() else selling.code,
            'selling_asset_issuer': selling.issuer,
            'buying_asset_type': buying.type,
            'buying_asset_code': None if buying.is_native() else buying.code,
            'buying_asset_issuer': buying.issuer,
        }
        self.params = {**self.params, **params}
