from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import AccountsCallBuilder
from tests.call_builder.call_builder_async import client, horizon_url


class TestAccountsCallBuilder:
    def test_init(self):
        builder = AccountsCallBuilder(horizon_url, client)
        assert builder.endpoint == "accounts"
        assert builder.params == {}

    def test_account(self):
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        builder = AccountsCallBuilder(horizon_url, client).account_id(account_id)

        assert builder.endpoint == "accounts/{}".format(account_id)
        assert builder.params == {}

    def test_for_signer(self):
        signer = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        builder = AccountsCallBuilder(horizon_url, client).for_signer(signer)
        assert builder.endpoint == "accounts"
        assert builder.params == {"signer": signer}

    def test_for_asset(self):
        asset = Asset("USD", "GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V")
        builder = AccountsCallBuilder(horizon_url, client).for_asset(asset)
        assert builder.endpoint == "accounts"
        assert builder.params == {
            "asset": "USD:GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V"
        }

    def test_for_sponsor(self):
        sponsor = "GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V"
        builder = AccountsCallBuilder(horizon_url, client).for_sponsor(sponsor)
        assert builder.endpoint == "accounts"
        assert builder.params == {"sponsor": sponsor}

    def test_for_liquidity_pool(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        builder = AccountsCallBuilder(horizon_url, client).for_liquidity_pool(
            liquidity_pool_id
        )
        assert builder.endpoint == "accounts"
        assert builder.params == {"liquidity_pool": liquidity_pool_id}
