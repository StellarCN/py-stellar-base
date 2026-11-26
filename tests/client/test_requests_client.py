from unittest.mock import MagicMock, patch

import pytest
import requests
from requests import RequestException

from stellar_sdk.client.requests_client import USER_AGENT, RequestsClient
from stellar_sdk.exceptions import (
    ConnectionError,
    ContentSizeLimitExceededError,
    StreamClientError,
)
from tests import _horizon_fixtures as hf


class TestRequestsClient:
    def test_get(self, httpbin_url):
        client = RequestsClient()
        url = httpbin_url + "get"
        params = {"hello": "world", "stellar": "sdk"}
        resp = client.get(url, params=params)
        assert resp.status_code == 200
        json = resp.json()
        assert json["args"] == params
        assert json["headers"]["User-Agent"] == USER_AGENT

    def test_post(self, httpbin_url):
        client = RequestsClient()
        url = httpbin_url + "post"
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

    @pytest.mark.parametrize(
        ("params", "cursor"), [(None, None), ({"cursor": "now"}, "now")]
    )
    def test_stream_error_before_the_first_event(self, params, cursor):
        client = RequestsClient()
        error = requests.ConnectionError("refused")
        with (
            patch("stellar_sdk.client.requests_client.EventSource", side_effect=error),
            pytest.raises(StreamClientError) as raised,
        ):
            next(client.stream("https://example.invalid", params))
        assert raised.value.current_cursor == cursor

    def test_stream(self, horizon_mock):
        client = RequestsClient()
        horizon_mock.expect(
            "/ledgers", body=hf.stream_body(), content_type="text/event-stream"
        )
        stream = client.stream(horizon_mock.url + "ledgers", {"cursor": "now"})
        try:
            assert next(stream) == {"id": "1"}
            assert next(stream) == {"id": "2"}
        finally:
            stream.close()

    def test_stream_uses_the_stream_session(self, horizon_mock):
        horizon_mock.expect(
            "/ledgers", body=hf.stream_body(), content_type="text/event-stream"
        )
        stream_session = requests.Session()
        stream_session.headers["Authorization"] = "Bearer token"
        client = RequestsClient(stream_session=stream_session)
        stream = client.stream(horizon_mock.url + "ledgers", {"cursor": "now"})
        try:
            assert next(stream) == {"id": "1"}
        finally:
            stream.close()
        ((request, _),) = horizon_mock.httpserver.log
        assert request.headers["Authorization"] == "Bearer token"
        assert f"stream_session={stream_session}" in repr(client)
        client.close()

    def test_with(self, httpbin_url):
        with RequestsClient() as client:
            url = httpbin_url + "get"
            params = {"hello": "world", "stellar": "sdk"}
            resp = client.get(url, params=params)
            assert resp.status_code == 200
            json = resp.json()
            assert json["args"] == params
            assert json["headers"]["User-Agent"] == USER_AGENT

    def test_custom_headers(self, httpbin_url):
        custom_headers = {"a": "b", "c": "d"}
        client = RequestsClient(custom_headers=custom_headers)
        url = httpbin_url + "get"
        params = {"hello": "world", "stellar": "sdk"}
        resp = client.get(url, params=params)
        assert resp.status_code == 200
        json = resp.json()
        assert json["args"] == params
        assert json["headers"]["User-Agent"] == USER_AGENT
        assert json["headers"]["A"] == custom_headers["a"]  # httpbin makes it upper
        assert json["headers"]["C"] == custom_headers["c"]

    def test_get_with_max_content_size_success(self, httpserver):
        client = RequestsClient()
        content = "Hello, World!"
        httpserver.expect_request("/data").respond_with_data(content)
        resp = client.get(httpserver.url_for("/data"), max_content_size=1024)
        assert resp.status_code == 200
        assert resp.text == content

    def test_get_with_max_content_size_exceeded(self, httpserver):
        client = RequestsClient()
        content = "x" * 1000
        httpserver.expect_request("/data").respond_with_data(content)
        with pytest.raises(ContentSizeLimitExceededError) as exc_info:
            client.get(httpserver.url_for("/data"), max_content_size=500)
        assert exc_info.value.limit == 500
        assert exc_info.value.content_size is not None
        assert exc_info.value.content_size > 500

    def test_get_without_max_content_size(self, httpserver):
        client = RequestsClient()
        content = "x" * 10000
        httpserver.expect_request("/data").respond_with_data(content)
        resp = client.get(httpserver.url_for("/data"))
        assert resp.status_code == 200
        assert resp.text == content

    def test_get_with_max_content_size_network_error_wraps_in_connection_error(self):
        """RequestException during streaming read should be wrapped in ConnectionError."""
        client = RequestsClient()
        with patch.object(client._session, "get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.iter_content.side_effect = RequestException("connection reset")
            mock_get.return_value = mock_resp
            with pytest.raises(ConnectionError):
                client.get("https://example.com/data", max_content_size=1024)
