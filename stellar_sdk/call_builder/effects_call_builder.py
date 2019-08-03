from ..call_builder.base_call_builder import BaseCallBuilder


class EffectsCallBuilder(BaseCallBuilder):
    def __init__(self, horizon_url, client):
        super().__init__(horizon_url, client)
        self.endpoint = "effects"

    def for_account(self, account_id):
        self.endpoint = "accounts/{account_id}/effects".format(account_id=account_id)
        return self

    def for_ledger(self, sequence):
        self.endpoint = "ledgers/{sequence}/effects".format(sequence=sequence)
        return self

    def for_transaction(self, transaction_hash):
        self.endpoint = "transactions/{transaction_hash}/effects".format(
            transaction_hash=transaction_hash
        )
        return self

    def for_operation(self, operation_id):
        self.endpoint = "operations/{operation_id}/effects".format(
            operation_id=operation_id
        )
        return self
