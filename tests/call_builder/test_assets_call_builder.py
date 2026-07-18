import pytest

from stellar_sdk.call_builder.call_builder_async import (
    AssetsCallBuilder as AssetsCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import AssetsCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (AssetsCallBuilder, SYNC_CLIENT),
        "async": (AssetsCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestAssetsCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "assets"
        assert builder.params == {}

    def test_for_code(self, builder_factory):
        asset_code = "BTC"
        builder = builder_factory().for_code(asset_code)
        assert builder.endpoint == "assets"
        assert builder.params == {"asset_code": asset_code}

    def test_for_issuer(self, builder_factory):
        asset_issuer = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"

        builder = builder_factory().for_issuer(asset_issuer)
        assert builder.endpoint == "assets"
        assert builder.params == {"asset_issuer": asset_issuer}

    def test_for_code_and_issuer(self, builder_factory):
        asset_code = "BTC"
        asset_issuer = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"

        builder = builder_factory().for_issuer(asset_issuer).for_code(asset_code)
        assert builder.endpoint == "assets"
        assert builder.params == {
            "asset_issuer": asset_issuer,
            "asset_code": asset_code,
        }
