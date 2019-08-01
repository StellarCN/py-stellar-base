from ..call_builder.base_call_builder import BaseCallBuilder


class AccountsCallBuilder(BaseCallBuilder):
    def __init__(self, horizon_url, client):
        super().__init__(horizon_url, client)
        self.endpoint = 'accounts'

    def account_id(self, account_id):
        self.endpoint = 'accounts/{account_id}'.format(account_id=account_id)
        return self
