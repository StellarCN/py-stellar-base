import pytest

from stellar_sdk.__version__ import __version__
from stellar_sdk.call_builder import BaseCallBuilder
from stellar_sdk.client.aiohttp_client import AiohttpClient
from stellar_sdk.client.requests_client import RequestsClient
from stellar_sdk.exceptions import BadRequestError, NotFoundError, NotPageableError


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
        ).raw_data

        assert resp["args"] == {"cursor": "89777", "limit": "25", "order": "asc"}
        assert resp["headers"][
            "User-Agent"
        ] == "py-stellar-sdk/{}/AiohttpClient".format(__version__)
        assert resp["headers"]["X-Client-Name"] == "py-stellar-sdk"
        assert resp["headers"]["X-Client-Version"] == __version__
        assert resp["url"] == "https://httpbin.org/get?cursor=89777&order=asc&limit=25"

    def test_get_data_sync(self):
        url = "https://httpbin.org/get"
        client = RequestsClient()
        resp = (
            BaseCallBuilder(url, client).limit(10).cursor(10086).order(desc=True).call()
        ).raw_data
        assert resp["args"] == {"cursor": "10086", "limit": "10", "order": "desc"}
        assert resp["headers"][
            "User-Agent"
        ] == "py-stellar-sdk/{}/RequestsClient".format(__version__)
        assert resp["headers"]["X-Client-Name"] == "py-stellar-sdk"
        assert resp["headers"]["X-Client-Version"] == __version__
        assert resp["url"] == "https://httpbin.org/get?limit=10&cursor=10086&order=desc"

    def _parse(self, raw_data):
        return raw_data

    @pytest.mark.slow
    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_get_stream_data_async(self):
        url = "https://horizon.stellar.org/ledgers"
        client = AiohttpClient()
        builder = BaseCallBuilder(url, client)
        builder._parse_response = self._parse
        resp = builder.cursor("now")._stream()
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
        builder = BaseCallBuilder(url, client)
        builder._parse_response = self._parse
        resp = builder.cursor("now")._stream()
        messages = []
        for msg in resp:
            assert isinstance(msg, dict)
            messages.append(msg)
            if len(messages) == 2:
                break

    def test_status_400_raise_sync(self):
        url = "https://horizon.stellar.org/accounts/BADACCOUNTID"
        client = RequestsClient()
        with pytest.raises(BadRequestError) as err:
            BaseCallBuilder(url, client).call()

        exception = err.value
        assert exception.status == 400
        assert exception.type == "https://stellar.org/horizon-errors/bad_request"
        assert exception.title == "Bad Request"
        assert exception.detail == "The request you sent was invalid in some way."
        assert exception.extras == {
            "invalid_field": "account_id",
            "reason": "invalid address",
        }

    def test_status_404_raise_sync(self):
        url = "https://horizon.stellar.org/not_found"
        client = RequestsClient()
        with pytest.raises(NotFoundError) as err:
            BaseCallBuilder(url, client).call()

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

    @pytest.mark.asyncio
    async def test_status_400_raise_async(self):
        url = "https://horizon.stellar.org/accounts/BADACCOUNTID"
        client = AiohttpClient()
        with pytest.raises(BadRequestError) as err:
            await BaseCallBuilder(url, client).call()

        exception = err.value
        assert exception.status == 400
        assert exception.type == "https://stellar.org/horizon-errors/bad_request"
        assert exception.title == "Bad Request"
        assert exception.detail == "The request you sent was invalid in some way."
        assert exception.extras == {
            "invalid_field": "account_id",
            "reason": "invalid address",
        }

    @pytest.mark.asyncio
    async def test_status_404_raise_async(self):
        url = "https://horizon.stellar.org/not_found"
        client = AiohttpClient()
        with pytest.raises(NotFoundError) as err:
            await BaseCallBuilder(url, client).call()

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

    def test_get_data_no_link(self):
        url = "https://httpbin.org/get"
        client = RequestsClient()
        call_builder = (
            BaseCallBuilder(url, client).limit(10).cursor(10086).order(desc=True)
        )
        call_builder.call()
        assert call_builder.next_href is None
        assert call_builder.prev_href is None

    def test_get_data_not_pageable_raise(self):
        url = "https://httpbin.org/get"
        client = RequestsClient()
        call_builder = (
            BaseCallBuilder(url, client).limit(10).cursor(10086).order(desc=True)
        )
        call_builder.call()
        with pytest.raises(NotPageableError, match="The next page does not exist."):
            call_builder.next()

        with pytest.raises(NotPageableError, match="The prev page does not exist."):
            call_builder.prev()

    def test_get_data_page(self):
        url = "https://horizon.stellar.org/transactions"
        client = RequestsClient()
        call_builder = (
            BaseCallBuilder(url, client)
            .cursor(81058917781504)
            .limit(10)
            .order(desc=True)
        )
        first_resp = call_builder.call().raw_data
        assert first_resp["_links"] == {
            "self": {
                "href": "https://horizon.stellar.org/transactions?cursor=81058917781504&limit=10&order=desc"
            },
            "next": {
                "href": "https://horizon.stellar.org/transactions?cursor=12884905984&limit=10&order=desc"
            },
            "prev": {
                "href": "https://horizon.stellar.org/transactions?cursor=80607946215424&limit=10&order=asc"
            },
        }
        next_resp = call_builder.next().raw_data
        assert next_resp["_links"] == {
            "self": {
                "href": "https://horizon.stellar.org/transactions?cursor=12884905984&limit=10&order=desc"
            },
            "next": {
                "href": "https://horizon.stellar.org/transactions?cursor=12884905984&limit=10&order=desc"
            },
            "prev": {
                "href": "https://horizon.stellar.org/transactions?cursor=12884905984&limit=10&order=asc"
            },
        }
        prev_page = call_builder.prev().raw_data
        assert prev_page["_links"] == {
            "self": {
                "href": "https://horizon.stellar.org/transactions?cursor=12884905984&limit=10&order=asc"
            },
            "next": {
                "href": "https://horizon.stellar.org/transactions?cursor=81827716927488&limit=10&order=asc"
            },
            "prev": {
                "href": "https://horizon.stellar.org/transactions?cursor=33676838572032&limit=10&order=desc"
            },
        }
