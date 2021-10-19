from stellar_sdk.call_builder.call_builder_sync import TransactionsCallBuilder
from tests.call_builder.call_builder_sync import client, horizon_url


class TestTransactionsCallBuilder:
    def test_init(self):
        builder = TransactionsCallBuilder(horizon_url, client)
        assert builder.endpoint == "transactions"
        assert builder.params == {}

    def test_transaction(self):
        transaction_hash = (
            "3389e9f0f1a65f19736cacf544c2e825313e8447f569233bb8db39aa607c8889"
        )
        builder = TransactionsCallBuilder(horizon_url, client).transaction(
            transaction_hash
        )
        assert builder.endpoint == "transactions/{transaction_hash}".format(
            transaction_hash=transaction_hash
        )
        assert builder.params == {}

    def test_for_account(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = TransactionsCallBuilder(horizon_url, client).for_account(account_id)
        assert builder.endpoint == "accounts/{account_id}/transactions".format(
            account_id=account_id
        )
        assert builder.params == {}

    def test_for_ledger(self):
        ledger = 123456
        builder = TransactionsCallBuilder(horizon_url, client).for_ledger(ledger)
        assert builder.endpoint == "ledgers/{ledger}/transactions".format(ledger=ledger)
        assert builder.params == {}

    def test_claimable_balance(self):
        claimable_balance_id = (
            "3389e9f0f1a65f19736cacf544c2e825313e8447f569233bb8db39aa607c8889"
        )
        builder = TransactionsCallBuilder(horizon_url, client).for_claimable_balance(
            claimable_balance_id
        )
        assert (
            builder.endpoint
            == "claimable_balances/{claimable_balance_id}/transactions".format(
                claimable_balance_id=claimable_balance_id
            )
        )
        assert builder.params == {}

    def test_for_liquidity_pool(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        builder = TransactionsCallBuilder(horizon_url, client).for_liquidity_pool(
            liquidity_pool_id
        )
        assert builder.endpoint == f"liquidity_pools/{liquidity_pool_id}/transactions"
        assert builder.params == {}

    def test_include_failed(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = (
            TransactionsCallBuilder(horizon_url, client)
            .for_account(account_id)
            .include_failed(True)
        )
        assert builder.endpoint == "accounts/{account_id}/transactions".format(
            account_id=account_id
        )
        assert builder.params == {"include_failed": "true"}

    def test_not_include_failed(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = (
            TransactionsCallBuilder(horizon_url, client)
            .for_account(account_id)
            .include_failed(False)
        )
        assert builder.endpoint == "accounts/{account_id}/transactions".format(
            account_id=account_id
        )
        assert builder.params == {"include_failed": "false"}
