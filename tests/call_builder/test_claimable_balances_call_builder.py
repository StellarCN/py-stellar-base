from stellar_sdk import Asset

from stellar_sdk.call_builder.claimable_balances_call_builder import (
    ClaimableBalancesCallBuilder,
)
from tests.call_builder import horizon_url, client


class TestClaimableBalancesCallBuilder:
    def test_init(self):
        builder = ClaimableBalancesCallBuilder(horizon_url, client)
        assert builder.endpoint == "claimable_balances"
        assert builder.params == {}

    def test_for_claimant(self):
        claimant = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = ClaimableBalancesCallBuilder(horizon_url, client).for_claimant(
            claimant
        )
        assert builder.endpoint == "claimable_balances"
        assert builder.params == {"claimant": claimant}

    def test_for_asset(self):
        asset = Asset("BTC", "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH")
        builder = ClaimableBalancesCallBuilder(horizon_url, client).for_asset(asset)
        assert builder.endpoint == "claimable_balances"
        assert builder.params == {
            "asset": "BTC:GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        }

    def test_for_sponsor(self):
        sponsor = "GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V"
        builder = ClaimableBalancesCallBuilder(horizon_url, client).for_sponsor(sponsor)
        assert builder.endpoint == "claimable_balances"
        assert builder.params == {"sponsor": sponsor}
