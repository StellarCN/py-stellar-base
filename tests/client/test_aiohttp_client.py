import pytest

from stellar_sdk.client.aiohttp_client import USER_AGENT, AiohttpClient
from tests import HTTPBIN_URL


@pytest.mark.slow
class TestAiohttpClient:
    @pytest.mark.asyncio
    async def test_get(self):
        user_agent = "Hello/Stellar/overcat"
        client = AiohttpClient(pool_size=10, user_agent=user_agent)
        url = HTTPBIN_URL + "get"
        params = {"hello": "world", "stellar": "sdk"}
        resp = await client.get(url, params=params)
        assert resp.status_code == 200
        json = resp.json()
        assert json["args"] == params
        assert json["headers"]["User-Agent"] == user_agent
        await client.close()

    @pytest.mark.asyncio
    async def test_post(self):
        client = AiohttpClient()
        url = HTTPBIN_URL + "post"
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

    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_stream(self):
        async with AiohttpClient() as client:
            resp = []
            async for msg in client.stream(
                "https://horizon.stellar.org/ledgers", {"cursor": "now"}
            ):
                assert isinstance(msg, dict)
                resp.append(msg)
                if len(resp) == 2:
                    break

    @pytest.mark.asyncio
    async def test_with(self):
        async with AiohttpClient() as client:
            url = HTTPBIN_URL + "get"
            params = {"hello": "world", "stellar": "sdk"}
            resp = await client.get(url, params=params)
            assert resp.status_code == 200
            json = resp.json()
            assert json["args"] == params
            assert json["headers"]["User-Agent"] == USER_AGENT

    @pytest.mark.asyncio
    async def test_custom_headers(self):
        user_agent = "Hello/Stellar/overcat"
        custom_headers = {"a": "b", "c": "d"}
        client = AiohttpClient(
            pool_size=10, user_agent=user_agent, custom_headers=custom_headers
        )
        url = HTTPBIN_URL + "get"
        params = {"hello": "world", "stellar": "sdk"}
        resp = await client.get(url, params=params)
        assert resp.status_code == 200
        json = resp.json()
        assert json["args"] == params
        assert json["headers"]["User-Agent"] == user_agent
        assert json["headers"]["A"] == custom_headers["a"]
        assert json["headers"]["C"] == custom_headers["c"]
        await client.close()
