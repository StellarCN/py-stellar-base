import pytest

from stellar_sdk.call_builder.call_builder_async import (
    LedgersCallBuilder as LedgersCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import LedgersCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (LedgersCallBuilder, SYNC_CLIENT),
        "async": (LedgersCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestLedgersCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "ledgers"
        assert builder.params == {}

    def test_ledger(self, builder_factory):
        ledger_id = 1714814
        builder = builder_factory().ledger(ledger_id)
        assert builder.endpoint == f"ledgers/{ledger_id}"
        assert builder.params == {}
