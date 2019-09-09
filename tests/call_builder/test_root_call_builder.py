from stellar_sdk.call_builder import RootCallBuilder
from tests.call_builder import horizon_url, client


class TestPaymentsCallBuilder:
    def test_init(self):
        builder = RootCallBuilder(horizon_url, client)
        assert builder.endpoint == ""
        assert builder.params == {}
