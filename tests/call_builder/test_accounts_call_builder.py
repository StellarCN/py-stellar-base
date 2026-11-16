import pytest

from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import (
    AccountsCallBuilder as AccountsCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import AccountsCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (AccountsCallBuilder, SYNC_CLIENT),
        "async": (AccountsCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestAccountsCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "accounts"
        assert builder.params == {}

    def test_account(self, builder_factory):
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        builder = builder_factory().account_id(account_id)

        assert builder.endpoint == f"accounts/{account_id}"
        assert builder.params == {}

    def test_for_signer(self, builder_factory):
        signer = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        builder = builder_factory().for_signer(signer)
        assert builder.endpoint == "accounts"
        assert builder.params == {"signer": signer}

    def test_for_asset(self, builder_factory):
        asset = Asset("USD", "GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V")
        builder = builder_factory().for_asset(asset)
        assert builder.endpoint == "accounts"
        assert builder.params == {
            "asset": "USD:GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V"
        }

    def test_for_sponsor(self, builder_factory):
        sponsor = "GAEDTJ4PPEFVW5XV2S7LUXBEHNQMX5Q2GM562RJGOQG7GVCE5H3HIB4V"
        builder = builder_factory().for_sponsor(sponsor)
        assert builder.endpoint == "accounts"
        assert builder.params == {"sponsor": sponsor}

    def test_for_liquidity_pool(self, builder_factory):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        builder = builder_factory().for_liquidity_pool(liquidity_pool_id)
        assert builder.endpoint == "accounts"
        assert builder.params == {"liquidity_pool": liquidity_pool_id}
