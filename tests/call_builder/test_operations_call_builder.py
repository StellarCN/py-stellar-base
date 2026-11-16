import pytest

from stellar_sdk.call_builder.call_builder_async import (
    OperationsCallBuilder as OperationsCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import OperationsCallBuilder
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (OperationsCallBuilder, SYNC_CLIENT),
        "async": (OperationsCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestOperationsCallBuilder:
    def test_init(self, builder_factory):
        builder = builder_factory()
        assert builder.endpoint == "operations"
        assert builder.params == {}

    def test_operation(self, builder_factory):
        operation_id = 2243214
        builder = builder_factory().operation(operation_id)
        assert builder.endpoint == f"operations/{operation_id}"
        assert builder.params == {}

    def test_for_account(self, builder_factory):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = builder_factory().for_account(account_id)
        assert builder.endpoint == f"accounts/{account_id}/operations"
        assert builder.params == {}

    def test_for_ledger(self, builder_factory):
        ledger = 123456
        builder = builder_factory().for_ledger(ledger)
        assert builder.endpoint == f"ledgers/{ledger}/operations"
        assert builder.params == {}

    def test_for_transaction(self, builder_factory):
        transaction_hash = (
            "3389e9f0f1a65f19736cacf544c2e825313e8447f569233bb8db39aa607c8889"
        )
        builder = builder_factory().for_transaction(transaction_hash)
        assert builder.endpoint == f"transactions/{transaction_hash}/operations"
        assert builder.params == {}

    def test_for_claimable_balance(self, builder_factory):
        claimable_balance_id = (
            "3389e9f0f1a65f19736cacf544c2e825313e8447f569233bb8db39aa607c8889"
        )
        builder = builder_factory().for_claimable_balance(claimable_balance_id)
        assert (
            builder.endpoint == f"claimable_balances/{claimable_balance_id}/operations"
        )
        assert builder.params == {}

    def test_for_liquidity_pool(self, builder_factory):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        builder = builder_factory().for_liquidity_pool(liquidity_pool_id)
        assert builder.endpoint == f"liquidity_pools/{liquidity_pool_id}/operations"
        assert builder.params == {}

    def test_include_failed(self, builder_factory):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = builder_factory().for_account(account_id).include_failed(True)
        assert builder.endpoint == f"accounts/{account_id}/operations"
        assert builder.params == {"include_failed": "true"}

    def test_not_include_failed(self, builder_factory):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = builder_factory().for_account(account_id).include_failed(False)
        assert builder.endpoint == f"accounts/{account_id}/operations"
        assert builder.params == {"include_failed": "false"}

    def test_join(self, builder_factory):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = (
            builder_factory()
            .for_account(account_id)
            .include_failed(False)
            .join("transactions")
        )
        assert builder.endpoint == f"accounts/{account_id}/operations"
        assert builder.params == {"include_failed": "false", "join": "transactions"}
