import pytest

from stellar_sdk.client.requests_client import USER_AGENT, RequestsClient
from tests import HTTPBIN_URL


@pytest.mark.slow
class TestRequestsClient:
    def test_get(self):
        client = RequestsClient()
        url = HTTPBIN_URL + "get"
        params = {"hello": "world", "stellar": "sdk"}
        resp = client.get(url, params=params)
        assert resp.status_code == 200
        json = resp.json()
        assert json["args"] == params
        assert json["headers"]["User-Agent"] == USER_AGENT

    def test_post(self):
        client = RequestsClient()
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

    @pytest.mark.timeout(30)
    def test_stream(self):
        client = RequestsClient()
        resp = []
        for msg in client.stream(
            "https://horizon.stellar.org/ledgers", {"cursor": "now"}
        ):
            assert isinstance(msg, dict)
            resp.append(msg)
            if len(resp) == 2:
                break

    def test_with(self):
        with RequestsClient() as client:
            url = HTTPBIN_URL + "get"
            params = {"hello": "world", "stellar": "sdk"}
            resp = client.get(url, params=params)
            assert resp.status_code == 200
            json = resp.json()
            assert json["args"] == params
            assert json["headers"]["User-Agent"] == USER_AGENT

    def test_custom_headers(self):
        custom_headers = {"a": "b", "c": "d"}
        client = RequestsClient(custom_headers=custom_headers)
        url = HTTPBIN_URL + "get"
        params = {"hello": "world", "stellar": "sdk"}
        resp = client.get(url, params=params)
        assert resp.status_code == 200
        json = resp.json()
        assert json["args"] == params
        assert json["headers"]["User-Agent"] == USER_AGENT
        assert json["headers"]["A"] == custom_headers["a"]  # httpbin makes it upper
        assert json["headers"]["C"] == custom_headers["c"]
