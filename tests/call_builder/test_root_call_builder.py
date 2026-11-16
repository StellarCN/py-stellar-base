import pytest

from stellar_sdk.call_builder.call_builder_async import (
    RootCallBuilder as RootCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import RootCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (RootCallBuilder, SYNC_CLIENT),
        "async": (RootCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestRootCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == ""
        assert builder.params == {}
