import pytest

from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import (
    OffersCallBuilder as OffersCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import OffersCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (OffersCallBuilder, SYNC_CLIENT),
        "async": (OffersCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestOffersCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "offers"
        assert builder.params == {}

    def test_for_offer(self, builder_factory):
        offer_id = "1000"
        builder = builder_factory()
        builder.offer(offer_id)
        assert builder.endpoint == f"offers/{offer_id}"
        assert builder.params == {}

    def test_for_asset(self, builder_factory):
        selling = Asset(
            "BTC", "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        )
        buying = Asset.native()
        builder = builder_factory()
        builder.for_selling(selling)
        builder.for_buying(buying)
        assert builder.endpoint == "offers"
        assert builder.params == {
            "selling_asset_type": selling.type,
            "selling_asset_code": selling.code,
            "selling_asset_issuer": selling.issuer,
            "buying_asset_type": buying.type,
        }

    def test_for_seller(self, builder_factory):
        seller = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        selling = Asset(
            "BTC", "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        )
        buying = Asset.native()
        builder = builder_factory()
        builder.for_seller(seller)
        builder.for_selling(selling)
        builder.for_buying(buying)
        assert builder.endpoint == "offers"
        assert builder.params == {
            "seller": seller,
            "selling_asset_type": selling.type,
            "selling_asset_code": selling.code,
            "selling_asset_issuer": selling.issuer,
            "buying_asset_type": buying.type,
        }

    def test_for_sponsor(self, builder_factory):
        sponsor = "GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V"
        builder = builder_factory().for_sponsor(sponsor)
        assert builder.endpoint == "offers"
        assert builder.params == {"sponsor": sponsor}

    def test_for_account(self, builder_factory):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = builder_factory().for_account(account_id)
        assert builder.endpoint == f"accounts/{account_id}/offers"
        assert builder.params == {}
