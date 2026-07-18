import pytest

from stellar_sdk import Asset
from stellar_sdk.call_builder.call_builder_async import (
    TradeAggregationsCallBuilder as TradeAggregationsCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import TradeAggregationsCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (TradeAggregationsCallBuilder, SYNC_CLIENT),
        "async": (TradeAggregationsCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestTradeAggregationsCallBuilder:
    def test_init(self, builder_factory):
        base = Asset("XCN", "GCOMOKXUA4TAEBB2QDHZD53SNRWKNTJMVEFLE47JYN5HS7KNLOABVA4Z")
        counter = Asset.native()
        resolution = 300000
        builder = builder_factory(base=base, counter=counter, resolution=resolution)
        assert builder.endpoint == "trade_aggregations"
        assert builder.params == {
            "base_asset_type": base.type,
            "base_asset_code": base.code,
            "base_asset_issuer": base.issuer,
            "counter_asset_type": counter.type,
            "resolution": str(resolution),
        }

    def test_invalid_resolution_raise(self, builder_factory):
        base = Asset("XCN", "GCOMOKXUA4TAEBB2QDHZD53SNRWKNTJMVEFLE47JYN5HS7KNLOABVA4Z")
        counter = Asset.native()
        resolution = 1000
        with pytest.raises(ValueError, match=f"Invalid resolution: {resolution}"):
            builder_factory(base=base, counter=counter, resolution=resolution)

    def test_invalid_offset_raise(self, builder_factory):
        base = Asset("XCN", "GCOMOKXUA4TAEBB2QDHZD53SNRWKNTJMVEFLE47JYN5HS7KNLOABVA4Z")
        counter = Asset.native()
        resolution = 300000
        offset = 600000
        with pytest.raises(ValueError, match=f"Invalid offset: {offset}"):
            builder_factory(
                base=base,
                counter=counter,
                resolution=resolution,
                offset=offset,
            )
