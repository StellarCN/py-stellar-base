from stellar_sdk.call_builder.call_builder_sync import FeeStatsCallBuilder
from tests.call_builder.call_builder_sync import client, horizon_url


class TestFeeStatsCallBuilder:
    def test_init(self):
        builder = FeeStatsCallBuilder(horizon_url, client)
        assert builder.endpoint == "fee_stats"
        assert builder.params == {}
