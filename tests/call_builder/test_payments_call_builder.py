import pytest

from stellar_sdk.call_builder.call_builder_async import (
    PaymentsCallBuilder as PaymentsCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import PaymentsCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (PaymentsCallBuilder, SYNC_CLIENT),
        "async": (PaymentsCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestPaymentsCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "payments"
        assert builder.params == {}

    def test_for_account(self, builder_factory):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = builder_factory().for_account(account_id)
        assert builder.endpoint == f"accounts/{account_id}/payments"
        assert builder.params == {}

    def test_for_ledger(self, builder_factory):
        ledger = 123456
        builder = builder_factory().for_ledger(ledger)
        assert builder.endpoint == f"ledgers/{ledger}/payments"
        assert builder.params == {}

    def test_for_transaction(self, builder_factory):
        transaction_hash = (
            "3389e9f0f1a65f19736cacf544c2e825313e8447f569233bb8db39aa607c8889"
        )

        builder = builder_factory().for_transaction(transaction_hash)
        assert builder.endpoint == f"transactions/{transaction_hash}/payments"
        assert builder.params == {}

    def test_include_failed(self, builder_factory):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = builder_factory().for_account(account_id).include_failed(True)
        assert builder.endpoint == f"accounts/{account_id}/payments"
        assert builder.params == {"include_failed": "true"}

    def test_not_include_failed(self, builder_factory):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = builder_factory().for_account(account_id).include_failed(False)
        assert builder.endpoint == f"accounts/{account_id}/payments"
        assert builder.params == {"include_failed": "false"}

    def test_join(self, builder_factory):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = (
            builder_factory()
            .for_account(account_id)
            .include_failed(False)
            .join("transactions")
        )
        assert builder.endpoint == f"accounts/{account_id}/payments"
        assert builder.params == {"include_failed": "false", "join": "transactions"}
