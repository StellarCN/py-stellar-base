from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder


class PathsCallBuilder(BaseCallBuilder):
    def __init__(
        self,
        horizon_url,
        client,
        source_account: str,
        destination_account: str,
        destination_asset: Asset,
        destination_amount: str,
    ):
        super().__init__(horizon_url, client)
        self.endpoint = "paths"
        params = {
            "destination_account": destination_account,
            "source_account": source_account,
            "destination_amount": destination_amount,
            "destination_asset_type": destination_asset.type,
            "destination_asset_code": None
            if destination_asset.is_native()
            else destination_asset.code,
            "destination_asset_issuer": destination_asset.issuer,
        }
        self.params = {**self.params, **params}
