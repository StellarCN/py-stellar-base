import pytest

from stellar_sdk.client.simple_requests_client import USER_AGENT, SimpleRequestsClient
from tests import HTTPBIN_URL


@pytest.mark.slow
class TestSimpleRequestsClient:
    def test_get(self):
        client = SimpleRequestsClient()
        url = HTTPBIN_URL + "get"
        params = {"hello": "world", "stellar": "sdk"}
        resp = client.get(url, params=params)
        assert resp.status_code == 200
        json = resp.json()
        assert json["args"] == params
        assert json["headers"]["User-Agent"] == USER_AGENT

    def test_post(self):
        client = SimpleRequestsClient()
        url = HTTPBIN_URL + "post"
        data = {
            "tx": "AAAAABa3N0+hJk17vP/AnYK5xV4o/PhOnEfgi36HlYo4g+3nAAAAZQFDfjoAAaTSAAAAAA"
            "AAAAEAAAAJX3VwZGF0ZWRfAAAAAAAAAQAAAAEAAAAAFrc3T6EmTXu8/8CdgrnFXij8+E6cR+"
            "CLfoeVijiD7ecAAAADAAAAAAAAAAFFVFgAAAAAAIhWSba8wLvB8YFRdzLJPkoyQSFmvRMQeaD"
            "Kym9JD6yTAAAAAAfjgC8NOvYPAA7nFwAAAAAGU5P1AAAAAAAAAAE4g+3nAAAAQOlPDNg4a76N/4"
            "VQh5oKc+RaUZVlK3Pr1HJphQn/yMthQh9gVGUbg/MHKl1RnKPuvmpzyqpBgb1zBVgyAYfIaQI="
        }
        resp = client.post(url, data=data)
        assert resp.status_code == 200
        json = resp.json()
        assert json["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert json["form"] == data

    def test_get_with_max_content_size_raises_not_implemented(self):
        client = SimpleRequestsClient()
        with pytest.raises(NotImplementedError) as exc_info:
            client.get("https://example.com", max_content_size=1024)
        assert "max_content_size is not supported" in str(exc_info.value)
        assert "RequestsClient" in str(exc_info.value)
