from ..call_builder.base_call_builder import BaseCallBuilder


class TransactionsCallBuilder(BaseCallBuilder):
    def __init__(self, horizon_url, client):
        super().__init__(horizon_url, client)
        self.endpoint = 'transactions'

    def transaction(self, transaction_id):
        self.endpoint = 'transactions/{transaction_id}'.format(transaction_id=transaction_id)

    def for_account(self, account_id):
        self.endpoint = 'accounts/{account_id}/transactions'.format(account_id=account_id)
        return self

    def for_ledger(self, sequence):
        self.endpoint = 'ledgers/{sequence}/transactions'.format(sequence=sequence)
        return self

    def include_failed(self, include_failed: bool):
        self.params['include_failed'] = include_failed
        return self
