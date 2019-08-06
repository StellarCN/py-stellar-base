import pytest

from stellar_sdk.call_builder import BaseCallBuilder
from stellar_sdk.client.requests_client import RequestsClient
from stellar_sdk.client.aiohttp_client import AiohttpClient
from stellar_sdk.__version__ import __version__


class TestBaseCallBuilder:
    @pytest.mark.asyncio
    async def test_get_data_async(self):
        url = "https://httpbin.org/get"
        client = AiohttpClient()
        resp = (
            await BaseCallBuilder(url, client)
            .cursor(89777)
            .order(desc=False)
            .limit(25)
            .call()
        )

        json = resp.json()
        assert json["args"] == {"cursor": "89777", "limit": "25", "order": "asc"}
        assert json["headers"] == {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "httpbin.org",
            "User-Agent": "py-stellar-sdk/{}/AiohttpClient".format(__version__),
            "X-Client-Name": "py-stellar-sdk",
            "X-Client-Version": __version__,
        }
        assert json["url"] == "https://httpbin.org/get?cursor=89777&order=asc&limit=25"

    def test_get_data_sync(self):
        url = "https://httpbin.org/get"
        client = RequestsClient()
        resp = (
            BaseCallBuilder(url, client).limit(10).cursor(10086).order(desc=True).call()
        )
        json = resp.json()
        assert json["args"] == {"cursor": "10086", "limit": "10", "order": "desc"}
        assert json["headers"] == {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Host": "httpbin.org",
            "User-Agent": "py-stellar-sdk/{}/RequestsClient".format(__version__),
            "X-Client-Name": "py-stellar-sdk",
            "X-Client-Version": __version__,
        }
        assert json["url"] == "https://httpbin.org/get?limit=10&cursor=10086&order=desc"

    @pytest.mark.slow
    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_get_stream_data_async(self):
        url = "https://horizon.stellar.org/ledgers"
        client = AiohttpClient()
        resp = BaseCallBuilder(url, client).cursor("now").stream()
        messages = []
        async for msg in resp:
            assert isinstance(msg, dict)
            messages.append(msg)
            if len(messages) == 2:
                break

    @pytest.mark.slow
    @pytest.mark.timeout(30)
    def test_stream_data_sync(self):
        url = "https://horizon.stellar.org/ledgers"
        client = RequestsClient()
        resp = BaseCallBuilder(url, client).cursor("now").stream()
        messages = []
        for msg in resp:
            assert isinstance(msg, dict)
            messages.append(msg)
            if len(messages) == 2:
                break
