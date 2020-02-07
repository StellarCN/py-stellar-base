from stellar_sdk import Asset

from stellar_sdk.call_builder import AccountsCallBuilder
from tests.call_builder import horizon_url, client


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

    def test_signer(self):
        signer = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        builder = AccountsCallBuilder(horizon_url, client).signer(signer)
        assert builder.endpoint == "accounts"
        assert builder.params == {"signer": signer}

    def test_asset(self):
        asset = Asset("USD", "GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V")
        builder = AccountsCallBuilder(horizon_url, client).asset(asset)
        assert builder.endpoint == "accounts"
        assert builder.params == {
            "asset": "USD:GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V"
        }
