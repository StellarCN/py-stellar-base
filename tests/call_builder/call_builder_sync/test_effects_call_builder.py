from stellar_sdk.call_builder.call_builder_sync import EffectsCallBuilder
from tests.call_builder.call_builder_sync import client, horizon_url


class TestEffectsCallBuilder:
    def test_init(self):
        builder = EffectsCallBuilder(horizon_url, client)
        assert builder.endpoint == "effects"
        assert builder.params == {}

    def test_for_account(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = EffectsCallBuilder(horizon_url, client).for_account(account_id)
        assert builder.endpoint == "accounts/{account_id}/effects".format(
            account_id=account_id
        )
        assert builder.params == {}

    def test_for_ledger(self):
        ledger = 123456
        builder = EffectsCallBuilder(horizon_url, client).for_ledger(ledger)
        assert builder.endpoint == "ledgers/{ledger}/effects".format(ledger=ledger)
        assert builder.params == {}

    def test_for_operation(self):
        operation = 969696
        builder = EffectsCallBuilder(horizon_url, client).for_operation(operation)
        assert builder.endpoint == "operations/{operation}/effects".format(
            operation=operation
        )
        assert builder.params == {}

    def test_for_transaction(self):
        transaction_hash = (
            "3389e9f0f1a65f19736cacf544c2e825313e8447f569233bb8db39aa607c8889"
        )

        builder = EffectsCallBuilder(horizon_url, client).for_transaction(
            transaction_hash
        )
        assert builder.endpoint == "transactions/{transaction}/effects".format(
            transaction=transaction_hash
        )
        assert builder.params == {}

    def test_for_liquidity_pool(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        builder = EffectsCallBuilder(horizon_url, client).for_liquidity_pool(
            liquidity_pool_id
        )
        assert builder.endpoint == f"liquidity_pools/{liquidity_pool_id}/effects"
        assert builder.params == {}
