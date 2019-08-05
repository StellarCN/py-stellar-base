from stellar_sdk.call_builder import LedgersCallBuilder
from tests.call_builder import horizon_url, client


class TestLedgersCallBuilder:
    def test_init(self):
        builder = LedgersCallBuilder(horizon_url, client)
        assert builder.endpoint == "ledgers"
        assert builder.params == {}

    def test_ledger(self):
        ledger_id = 1714814
        builder = LedgersCallBuilder(horizon_url, client).ledger(ledger_id)
        assert builder.endpoint == "ledgers/{ledger}".format(ledger=ledger_id)
        assert builder.params == {}
