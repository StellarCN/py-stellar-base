from ..call_builder.base_call_builder import BaseCallBuilder


class AssetsCallBuilder(BaseCallBuilder):
    def __init__(self, horizon_url, client):
        super().__init__(horizon_url, client)
        self.endpoint = 'assets'

    def for_code(self, code: str):
        self.params['asset_code'] = code
        return self

    def for_issuer(self, issuer: str):
        self.params['asset_issuer'] = issuer
        return self
