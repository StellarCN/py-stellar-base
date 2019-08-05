from stellar_sdk import Asset
from stellar_sdk.call_builder import PathsCallBuilder
from tests.call_builder import horizon_url, client


class TestPathsCallBuilder:
    def test_init(self):
        source_account = "GCOMOKXUA4TAEBB2QDHZD53SNRWKNTJMVEFLE47JYN5HS7KNLOABVA4Z"
        destination_account = "GBSHJKHCXZ4OCFT44UVNEERGIM25NCHXCLA6MUXMTNIOQ5UHV22X4H2R"
        destination_asset = Asset(
            "USD", "GAMLPCLHQMS4GOHBUXHLWVKUIKOZSHYPIOO54EMSWGHBUJBO4S5T2MGG"
        )
        destination_amount = "1000.0"

        builder = PathsCallBuilder(
            horizon_url,
            client,
            source_account=source_account,
            destination_account=destination_account,
            destination_asset=destination_asset,
            destination_amount=destination_amount,
        )

        assert builder.endpoint == "paths"
        assert builder.params == {
            "destination_account": destination_account,
            "source_account": source_account,
            "destination_amount": destination_amount,
            "destination_asset_type": destination_asset.type,
            "destination_asset_issuer": destination_asset.issuer,
            "destination_asset_code": destination_asset.code,
        }
