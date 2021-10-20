from stellar_sdk.call_builder.call_builder_sync import AssetsCallBuilder
from tests.call_builder.call_builder_sync import client, horizon_url


class TestAssetsCallBuilder:
    def test_init(self):
        builder = AssetsCallBuilder(horizon_url, client)
        assert builder.endpoint == "assets"
        assert builder.params == {}

    def test_for_code(self):
        asset_code = "BTC"
        builder = AssetsCallBuilder(horizon_url, client).for_code(asset_code)
        assert builder.endpoint == "assets"
        assert builder.params == {"asset_code": asset_code}

    def test_for_issuer(self):
        asset_issuer = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"

        builder = AssetsCallBuilder(horizon_url, client).for_issuer(asset_issuer)
        assert builder.endpoint == "assets"
        assert builder.params == {"asset_issuer": asset_issuer}

    def test_for_code_and_issuer(self):
        asset_code = "BTC"
        asset_issuer = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"

        builder = (
            AssetsCallBuilder(horizon_url, client)
            .for_issuer(asset_issuer)
            .for_code(asset_code)
        )
        assert builder.endpoint == "assets"
        assert builder.params == {
            "asset_issuer": asset_issuer,
            "asset_code": asset_code,
        }
