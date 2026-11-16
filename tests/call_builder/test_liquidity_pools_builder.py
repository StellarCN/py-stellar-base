import pytest

from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import (
    LiquidityPoolsBuilder as LiquidityPoolsBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import LiquidityPoolsBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (LiquidityPoolsBuilder, SYNC_CLIENT),
        "async": (LiquidityPoolsBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestLiquidityPoolsBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "liquidity_pools"
        assert builder.params == {}

    def test_ledger(self, builder_factory):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        builder = builder_factory().liquidity_pool(liquidity_pool_id)
        assert builder.endpoint == f"liquidity_pools/{liquidity_pool_id}"
        assert builder.params == {}

    def test_for_reserves(self, builder_factory):
        reserves = [
            Asset("EURT", "GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S"),
            Asset("PHP", "GBUQWP3BOUZX34TOND2QV7QQ7K7VJTG6VSE7WMLBTMDJLLAW7YKGU6EP"),
        ]
        builder = builder_factory().for_reserves(reserves)
        assert builder.endpoint == "liquidity_pools"
        assert builder.params == {
            "reserves": "EURT:GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S,PHP:GBUQWP3BOUZX34TOND2QV7QQ7K7VJTG6VSE7WMLBTMDJLLAW7YKGU6EP"
        }

    def test_for_account(self, builder_factory):
        account_id = "GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S"
        builder = builder_factory().for_account(account_id)
        assert builder.endpoint == "liquidity_pools"
        assert builder.params == {"account": account_id}
