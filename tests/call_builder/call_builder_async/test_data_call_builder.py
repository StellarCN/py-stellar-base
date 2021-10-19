from stellar_sdk.call_builder.call_builder_async import DataCallBuilder
from tests.call_builder.call_builder_async import client, horizon_url


class TestDataCallBuilder:
    def test_init(self):
        account_id = "GBDBZR2B6RMSCYJ2A3XEFNKIB2KMNIUAMFE43MN46STT2DUIIGKGA5O3"
        data_name = "python_sdk"
        builder = DataCallBuilder(horizon_url, client, account_id, data_name)
        assert builder.endpoint == "/accounts/{account}/data/{key}".format(
            account=account_id, key=data_name
        )
        assert builder.params == {}
