from stellar_sdk.call_builder.call_builder_async import PaymentsCallBuilder
from tests.call_builder.call_builder_async import client, horizon_url


class TestPaymentsCallBuilder:
    def test_init(self):
        builder = PaymentsCallBuilder(horizon_url, client)
        assert builder.endpoint == "payments"
        assert builder.params == {}

    def test_for_account(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = PaymentsCallBuilder(horizon_url, client).for_account(account_id)
        assert builder.endpoint == "accounts/{account_id}/payments".format(
            account_id=account_id
        )
        assert builder.params == {}

    def test_for_ledger(self):
        ledger = 123456
        builder = PaymentsCallBuilder(horizon_url, client).for_ledger(ledger)
        assert builder.endpoint == "ledgers/{ledger}/payments".format(ledger=ledger)
        assert builder.params == {}

    def test_for_transaction(self):
        transaction_hash = (
            "3389e9f0f1a65f19736cacf544c2e825313e8447f569233bb8db39aa607c8889"
        )

        builder = PaymentsCallBuilder(horizon_url, client).for_transaction(
            transaction_hash
        )
        assert builder.endpoint == "transactions/{transaction}/payments".format(
            transaction=transaction_hash
        )
        assert builder.params == {}

    def test_include_failed(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = (
            PaymentsCallBuilder(horizon_url, client)
            .for_account(account_id)
            .include_failed(True)
        )
        assert builder.endpoint == "accounts/{account_id}/payments".format(
            account_id=account_id
        )
        assert builder.params == {"include_failed": "true"}

    def test_not_include_failed(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = (
            PaymentsCallBuilder(horizon_url, client)
            .for_account(account_id)
            .include_failed(False)
        )
        assert builder.endpoint == "accounts/{account_id}/payments".format(
            account_id=account_id
        )
        assert builder.params == {"include_failed": "false"}

    def test_join(self):
        account_id = "GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"
        builder = (
            PaymentsCallBuilder(horizon_url, client)
            .for_account(account_id)
            .include_failed(False)
            .join("transactions")
        )
        assert builder.endpoint == "accounts/{account_id}/payments".format(
            account_id=account_id
        )
        assert builder.params == {"include_failed": "false", "join": "transactions"}
