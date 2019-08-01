from ..call_builder.base_call_builder import BaseCallBuilder


class LedgersCallBuilder(BaseCallBuilder):
    def __init__(self, horizon_url, client):
        super().__init__(horizon_url, client)
        self.endpoint = 'ledgers'

    def ledger(self, sequence):
        self.endpoint = 'ledgers/{sequence}'.format(sequence=sequence)
        return self
