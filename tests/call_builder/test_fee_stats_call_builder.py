import pytest

from stellar_sdk.call_builder.call_builder_async import (
    FeeStatsCallBuilder as FeeStatsCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import FeeStatsCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (FeeStatsCallBuilder, SYNC_CLIENT),
        "async": (FeeStatsCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestFeeStatsCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "fee_stats"
        assert builder.params == {}
