from stellar_sdk.call_builder import RootCallBuilder
from tests.call_builder import client, horizon_url


class TestRootCallBuilder:
    def test_init(self):
        builder = RootCallBuilder(horizon_url, client)
        assert builder.endpoint == ""
        assert builder.params == {}
