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
