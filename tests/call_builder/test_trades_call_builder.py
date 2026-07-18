import pytest

from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import (
    TradesCallBuilder as TradesCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import TradesCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (TradesCallBuilder, SYNC_CLIENT),
        "async": (TradesCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestTradesCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "trades"
        assert builder.params == {}

    def test_for_offer(self, builder_factory):
        offer_id = 1233453
        builder = builder_factory().for_offer(offer_id)
        assert builder.endpoint == f"offers/{offer_id}/trades"
        assert builder.params == {}

    def test_for_account(self, builder_factory):
        account_id = "GCOMOKXUA4TAEBB2QDHZD53SNRWKNTJMVEFLE47JYN5HS7KNLOABVA4Z"
        builder = builder_factory().for_account(account_id)
        assert builder.endpoint == f"accounts/{account_id}/trades"
        assert builder.params == {}

    def test_for_asset_pair(self, builder_factory):
        base = Asset("XCN", "GCOMOKXUA4TAEBB2QDHZD53SNRWKNTJMVEFLE47JYN5HS7KNLOABVA4Z")
        counter = Asset.native()
        builder = builder_factory().for_asset_pair(base=base, counter=counter)
        assert builder.endpoint == "trades"
        assert builder.params == {
            "base_asset_type": base.type,
            "base_asset_code": base.code,
            "base_asset_issuer": base.issuer,
            "counter_asset_type": counter.type,
        }

    def test_for_trade_type(self, builder_factory):
        trade_type = "liquidity_pools"
        builder = builder_factory().for_trade_type(trade_type)
        assert builder.endpoint == "trades"
        assert builder.params == {
            "trade_type": trade_type,
        }

    def test_for_liquidity_pool(self, builder_factory):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        builder = builder_factory().for_liquidity_pool(liquidity_pool_id)
        assert builder.endpoint == f"liquidity_pools/{liquidity_pool_id}/trades"
        assert builder.params == {}
