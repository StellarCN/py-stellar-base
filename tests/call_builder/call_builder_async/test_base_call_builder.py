import pytest

from stellar_sdk.__version__ import __version__
from stellar_sdk.call_builder.call_builder_async import BaseCallBuilder
from stellar_sdk.client.aiohttp_client import AiohttpClient
from stellar_sdk.exceptions import BadRequestError, NotFoundError, NotPageableError
from tests import HTTPBIN_URL


@pytest.mark.slow
@pytest.mark.asyncio
class TestBaseCallBuilder:
    async def test_get_data(self):
        url = HTTPBIN_URL + "get"
        client = AiohttpClient()
        resp = (
            await BaseCallBuilder(horizon_url=url, client=client)
            .cursor(89777)
            .order(desc=False)
            .limit(25)
            .call()
        )

        assert resp["args"] == {"cursor": "89777", "limit": "25", "order": "asc"}
        assert resp["headers"][
            "User-Agent"
        ] == "py-stellar-base/{}/AiohttpClient".format(__version__)
        assert resp["headers"]["X-Client-Name"] == "py-stellar-base"
        assert resp["headers"]["X-Client-Version"] == __version__
        assert resp["url"] == HTTPBIN_URL + "get?cursor=89777&order=asc&limit=25"

    @pytest.mark.timeout(30)
    async def test_get_stream_data(self):
        url = "https://horizon.stellar.org/ledgers"
        client = AiohttpClient()
        resp = BaseCallBuilder(horizon_url=url, client=client).cursor("now").stream()
        messages = []
        async for msg in resp:
            assert isinstance(msg, dict)
            messages.append(msg)
            if len(messages) == 2:
                break

    async def test_status_400_raise(self):
        url = "https://horizon.stellar.org/accounts/BADACCOUNTID"
        client = AiohttpClient()
        with pytest.raises(BadRequestError) as err:
            await BaseCallBuilder(horizon_url=url, client=client).call()

        exception = err.value
        assert exception.status == 400
        assert exception.type == "https://stellar.org/horizon-errors/bad_request"
        assert exception.title == "Bad Request"
        assert exception.detail == "The request you sent was invalid in some way."
        assert exception.extras == {
            "invalid_field": "account_id",
            "reason": "Account ID must start with `G` and contain 56 alphanum characters",
        }

    async def test_status_404_raise(self):
        url = "https://horizon.stellar.org/not_found"
        client = AiohttpClient()
        with pytest.raises(NotFoundError) as err:
            await BaseCallBuilder(horizon_url=url, client=client).call()

        exception = err.value
        assert exception.status == 404
        assert exception.type == "https://stellar.org/horizon-errors/not_found"
        assert exception.title == "Resource Missing"
        assert (
            exception.detail
            == "The resource at the url requested was not found.  This "
            "usually occurs for one of two reasons:  The url requested is not valid, "
            "or no data in our database could be found with the parameters provided."
        )
        assert exception.extras is None

    async def test_get_data_no_link(self):
        url = HTTPBIN_URL + "get"
        client = AiohttpClient()
        call_builder = (
            BaseCallBuilder(horizon_url=url, client=client)
            .limit(10)
            .cursor(10086)
            .order(desc=True)
        )
        await call_builder.call()
        assert call_builder.next_href is None
        assert call_builder.prev_href is None
        await client.close()

    async def test_get_data_not_pageable_raise(self):
        url = HTTPBIN_URL + "get"
        client = AiohttpClient()
        call_builder = (
            BaseCallBuilder(horizon_url=url, client=client)
            .limit(10)
            .cursor(10086)
            .order(desc=True)
        )
        await call_builder.call()
        with pytest.raises(NotPageableError, match="The next page does not exist."):
            await call_builder.next()

        with pytest.raises(NotPageableError, match="The prev page does not exist."):
            await call_builder.prev()

        await client.close()

    async def test_get_data_page(self):
        url = "https://horizon.stellar.org/transactions"
        client = AiohttpClient()
        call_builder = (
            BaseCallBuilder(horizon_url=url, client=client).limit(10).order(desc=True)
        )
        first_resp = await call_builder.call()
        assert (
            first_resp["_links"]["self"]["href"]
            == "https://horizon.stellar.org/transactions?cursor=&limit=10&order=desc"
        )

        next_url = first_resp["_links"]["next"]["href"]
        next_url_cursor = next_url.split("cursor=")[1].split("&")[0]

        next_resp = await call_builder.next()
        assert next_resp["_links"]["self"][
            "href"
        ] == "https://horizon.stellar.org/transactions?cursor={}&limit=10&order=desc".format(
            next_url_cursor
        )

        prev_url = next_resp["_links"]["prev"]["href"]
        prev_url_cursor = prev_url.split("cursor=")[1].split("&")[0]
        prev_page = await call_builder.prev()
        assert prev_page["_links"]["self"][
            "href"
        ] == "https://horizon.stellar.org/transactions?cursor={}&limit=10&order=asc".format(
            prev_url_cursor
        )
        await client.close()

    async def test_horizon_url_params(self):
        url = HTTPBIN_URL + "get?version=1.2&auth=myPassw0wd"
        client = AiohttpClient()
        resp = (
            await BaseCallBuilder(horizon_url=url, client=client)
            .limit(10)
            .cursor(10086)
            .order(desc=True)
            .call()
        )
        assert resp["args"] == {
            "auth": "myPassw0wd",
            "cursor": "10086",
            "limit": "10",
            "order": "desc",
            "version": "1.2",
        }
        assert resp["headers"][
            "User-Agent"
        ] == "py-stellar-base/{}/AiohttpClient".format(__version__)
        assert resp["headers"]["X-Client-Name"] == "py-stellar-base"
        assert resp["headers"]["X-Client-Version"] == __version__
        assert (
            resp["url"]
            == HTTPBIN_URL
            + "get?version=1.2&auth=myPassw0wd&limit=10&cursor=10086&order=desc"
        )
        await client.close()
