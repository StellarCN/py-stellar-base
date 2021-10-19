from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_sync import ClaimableBalancesCallBuilder
from tests.call_builder.call_builder_sync import client, horizon_url


class TestClaimableBalancesCallBuilder:
    def test_init(self):
        builder = ClaimableBalancesCallBuilder(horizon_url, client)
        assert builder.endpoint == "claimable_balances"
        assert builder.params == {}

    def test_claimable_balance(self):
        claimable_balance_id = (
            "0000000043d380c38a2f2cac46ab63674064c56fdce6b977fdef1a278ad50e1a7e6a5e18"
        )
        builder = ClaimableBalancesCallBuilder(horizon_url, client).claimable_balance(
            claimable_balance_id
        )

        assert builder.endpoint == f"claimable_balances/{claimable_balance_id}"
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
