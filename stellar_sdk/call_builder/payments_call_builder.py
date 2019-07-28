from ..call_builder.base_call_builder import BaseCallBuilder


class PaymentsCallBuilder(BaseCallBuilder):
    def __init__(self, horizon_url, client):
        super().__init__(horizon_url, client)
        self.endpoint = 'payments'

    def for_account(self, account_id):
        self.endpoint = 'accounts/{account_id}/payments'.format(account_id=account_id)
        return self

    def for_ledger(self, sequence):
        self.endpoint = 'ledgers/{sequence}/payments'.format(sequence=sequence)
        return self

    def for_transaction(self, transaction_hash):
        self.endpoint = 'transactions/{transaction_hash}/payments'.format(transaction_hash=transaction_hash)
        return self
