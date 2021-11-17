from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import LiquidityPoolsBuilder
from tests.call_builder.call_builder_async import client, horizon_url


class TestLiquidityPoolsBuilder:
    def test_init(self):
        builder = LiquidityPoolsBuilder(horizon_url, client)
        assert builder.endpoint == "liquidity_pools"
        assert builder.params == {}

    def test_ledger(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        builder = LiquidityPoolsBuilder(horizon_url, client).liquidity_pool(
            liquidity_pool_id
        )
        assert builder.endpoint == f"liquidity_pools/{liquidity_pool_id}"
        assert builder.params == {}

    def test_for_reserves(self):
        reserves = [
            Asset("EURT", "GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S"),
            Asset("PHP", "GBUQWP3BOUZX34TOND2QV7QQ7K7VJTG6VSE7WMLBTMDJLLAW7YKGU6EP"),
        ]
        builder = LiquidityPoolsBuilder(horizon_url, client).for_reserves(reserves)
        assert builder.endpoint == f"liquidity_pools"
        assert builder.params == {
            "reserves": "EURT:GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S,PHP:GBUQWP3BOUZX34TOND2QV7QQ7K7VJTG6VSE7WMLBTMDJLLAW7YKGU6EP"
        }

    def test_for_account(self):
        account_id = "GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S"
        builder = LiquidityPoolsBuilder(horizon_url, client).for_account(account_id)
        assert builder.endpoint == f"liquidity_pools"
        assert builder.params == {"account": account_id}
