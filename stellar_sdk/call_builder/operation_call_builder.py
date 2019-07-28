from ..call_builder.base_call_builder import BaseCallBuilder


class OperationCallBuilder(BaseCallBuilder):
    def __init__(self, horizon_url, client):
        super().__init__(horizon_url, client)
        self.endpoint = 'operations'

    def operation(self, operation_id):
        self.endpoint = 'operations/{operation_id}'.format(operation_id=operation_id)

    def for_account(self, account_id):
        self.endpoint = 'accounts/{account_id}/operations'.format(account_id=account_id)
        return self

    def for_ledger(self, sequence):
        self.endpoint = 'ledgers/{sequence}/operations'.format(sequence=sequence)
        return self

    def for_transaction(self, transaction_hash):
        self.endpoint = 'transactions/{transaction_hash}/operations'.format(transaction_hash=transaction_hash)
        return self

    def include_failed(self, include_failed: bool):
        self.params['include_failed'] = include_failed
        return self
