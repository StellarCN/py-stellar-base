from unittest.mock import Mock

import pytest

from stellar_sdk.call_builder.call_builder_async import (
    DataCallBuilder as DataCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import DataCallBuilder
from stellar_sdk.client.base_sync_client import BaseSyncClient
from stellar_sdk.client.response import Response
from tests.call_builder import ASYNC_CLIENT, HORIZON_URL, SYNC_CLIENT


@pytest.fixture(params=["sync", "async"])
def builder_factory(request: pytest.FixtureRequest):
    builder_cls, client = {
        "sync": (DataCallBuilder, SYNC_CLIENT),
        "async": (DataCallBuilderAsync, ASYNC_CLIENT),
    }[request.param]

    def factory(*args, **kwargs):
        return builder_cls(HORIZON_URL, client, *args, **kwargs)

    return factory


class TestDataCallBuilder:
    def test_init(self, builder_factory):
        account_id = "GBDBZR2B6RMSCYJ2A3XEFNKIB2KMNIUAMFE43MN46STT2DUIIGKGA5O3"
        data_name = "python_sdk"
        builder = builder_factory(account_id, data_name)
        assert builder.endpoint == f"accounts/{account_id}/data/{data_name}"
        assert builder.params == {}

    @pytest.mark.parametrize(
        "horizon_url", ["https://example.org/horizon", "https://example.org/horizon/"]
    )
    def test_call_keeps_the_path_of_the_horizon_url(self, horizon_url):
        account_id = "GBDBZR2B6RMSCYJ2A3XEFNKIB2KMNIUAMFE43MN46STT2DUIIGKGA5O3"
        client = Mock(spec=BaseSyncClient)
        client.get.return_value = Response(200, "{}", {}, "")
        DataCallBuilder(horizon_url, client, account_id, "profile").call()
        url = client.get.call_args.args[0]
        assert url == f"https://example.org/horizon/accounts/{account_id}/data/profile"
