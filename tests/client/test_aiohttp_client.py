import pytest

from stellar_sdk.client.aiohttp_client import USER_AGENT, AiohttpClient
from stellar_sdk.exceptions import ConnectionError, ContentSizeLimitExceededError
from tests import _horizon_fixtures as hf


class TestAiohttpClient:
    async def test_get(self, httpbin_url):
        user_agent = "Hello/Stellar/overcat"
        client = AiohttpClient(pool_size=10, user_agent=user_agent)
        url = httpbin_url + "get"
        params = {"hello": "world", "stellar": "sdk"}
        resp = await client.get(url, params=params)
        assert resp.status_code == 200
        json = resp.json()
        assert json["args"] == params
        assert json["headers"]["User-Agent"] == user_agent
        await client.close()

    async def test_post(self, httpbin_url):
        client = AiohttpClient()
        url = httpbin_url + "post"
        data = {
            "tx": "AAAAABa3N0+hJk17vP/AnYK5xV4o/PhOnEfgi36HlYo4g+3nAAAAZQFDfjoAAaTSAAAAAA"
            "AAAAEAAAAJX3VwZGF0ZWRfAAAAAAAAAQAAAAEAAAAAFrc3T6EmTXu8/8CdgrnFXij8+E6cR+"
            "CLfoeVijiD7ecAAAADAAAAAAAAAAFFVFgAAAAAAIhWSba8wLvB8YFRdzLJPkoyQSFmvRMQeaD"
            "Kym9JD6yTAAAAAAfjgC8NOvYPAA7nFwAAAAAGU5P1AAAAAAAAAAE4g+3nAAAAQOlPDNg4a76N/4"
            "VQh5oKc+RaUZVlK3Pr1HJphQn/yMthQh9gVGUbg/MHKl1RnKPuvmpzyqpBgb1zBVgyAYfIaQI="
        }
        resp = await client.post(url, data=data)
        assert resp.status_code == 200
        json = resp.json()
        assert json["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert json["form"] == data
        await client.close()

    async def test_stream(self, horizon_mock):
        horizon_mock.expect(
            "/ledgers", body=hf.stream_body(), content_type="text/event-stream"
        )
        async with AiohttpClient() as client:
            stream = client.stream(horizon_mock.url + "ledgers", {"cursor": "now"})
            try:
                assert await anext(stream) == {"id": "1"}
                assert await anext(stream) == {"id": "2"}
            finally:
                await stream.aclose()

    async def test_with(self, httpbin_url):
        async with AiohttpClient() as client:
            url = httpbin_url + "get"
            params = {"hello": "world", "stellar": "sdk"}
            resp = await client.get(url, params=params)
            assert resp.status_code == 200
            json = resp.json()
            assert json["args"] == params
            assert json["headers"]["User-Agent"] == USER_AGENT

    async def test_custom_headers(self, httpbin_url):
        user_agent = "Hello/Stellar/overcat"
        custom_headers = {"a": "b", "c": "d"}
        client = AiohttpClient(
            pool_size=10, user_agent=user_agent, custom_headers=custom_headers
        )
        url = httpbin_url + "get"
        params = {"hello": "world", "stellar": "sdk"}
        resp = await client.get(url, params=params)
        assert resp.status_code == 200
        json = resp.json()
        assert json["args"] == params
        assert json["headers"]["User-Agent"] == user_agent
        assert json["headers"]["A"] == custom_headers["a"]
        assert json["headers"]["C"] == custom_headers["c"]
        await client.close()

    async def test_get_with_max_content_size_success(self, httpserver):
        content = "Hello, World!"
        httpserver.expect_request("/data").respond_with_data(content)
        async with AiohttpClient() as client:
            resp = await client.get(httpserver.url_for("/data"), max_content_size=1024)
            assert resp.status_code == 200
            assert resp.text == content

    async def test_get_with_max_content_size_exceeded(self, httpserver):
        content = "x" * 1000
        httpserver.expect_request("/data").respond_with_data(content)
        async with AiohttpClient() as client:
            with pytest.raises(ContentSizeLimitExceededError) as exc_info:
                await client.get(httpserver.url_for("/data"), max_content_size=500)
            assert exc_info.value.limit == 500
            assert exc_info.value.content_size is not None
            assert exc_info.value.content_size > 500

    async def test_get_without_max_content_size(self, httpserver):
        content = "x" * 10000
        httpserver.expect_request("/data").respond_with_data(content)
        async with AiohttpClient() as client:
            resp = await client.get(httpserver.url_for("/data"))
            assert resp.status_code == 200
            assert resp.text == content

    async def test_get_with_max_content_size_network_error_wraps_in_connection_error(
        self,
    ):
        """aiohttp.ClientError (e.g. connection refused) is wrapped in ConnectionError."""
        async with AiohttpClient() as client:
            with pytest.raises(ConnectionError):
                # Port 1 is never listening locally: the connection is refused.
                await client.get("http://127.0.0.1:1/data", max_content_size=1024)
