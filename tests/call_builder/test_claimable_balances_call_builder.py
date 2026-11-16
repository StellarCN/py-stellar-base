import pytest

from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import (
    ClaimableBalancesCallBuilder as ClaimableBalancesCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import ClaimableBalancesCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (ClaimableBalancesCallBuilder, SYNC_CLIENT),
        "async": (ClaimableBalancesCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestClaimableBalancesCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "claimable_balances"
        assert builder.params == {}

    def test_claimable_balance(self, builder_factory):
        claimable_balance_id = (
            "0000000043d380c38a2f2cac46ab63674064c56fdce6b977fdef1a278ad50e1a7e6a5e18"
        )
        builder = builder_factory().claimable_balance(claimable_balance_id)

        assert builder.endpoint == f"claimable_balances/{claimable_balance_id}"
        assert builder.params == {}

    def test_for_claimant(self, builder_factory):
        claimant = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = builder_factory().for_claimant(claimant)
        assert builder.endpoint == "claimable_balances"
        assert builder.params == {"claimant": claimant}

    def test_for_asset(self, builder_factory):
        asset = Asset("BTC", "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH")
        builder = builder_factory().for_asset(asset)
        assert builder.endpoint == "claimable_balances"
        assert builder.params == {
            "asset": "BTC:GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        }

    def test_for_sponsor(self, builder_factory):
        sponsor = "GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V"
        builder = builder_factory().for_sponsor(sponsor)
        assert builder.endpoint == "claimable_balances"
        assert builder.params == {"sponsor": sponsor}
