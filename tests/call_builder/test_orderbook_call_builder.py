import pytest

from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import (
    OrderbookCallBuilder as OrderbookCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import OrderbookCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (OrderbookCallBuilder, SYNC_CLIENT),
        "async": (OrderbookCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestOrderbookCallBuilder:
    def test_init(self, builder_factory):
        selling = Asset(
            "BTC", "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        )
        buying = Asset.native()
        builder = builder_factory(selling, buying)
        assert builder.endpoint == "order_book"
        assert builder.params == {
            "selling_asset_type": selling.type,
            "selling_asset_code": selling.code,
            "selling_asset_issuer": selling.issuer,
            "buying_asset_type": buying.type,
        }
