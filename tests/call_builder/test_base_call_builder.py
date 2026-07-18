from collections.abc import AsyncGenerator, AsyncIterator, Callable

import pytest

from stellar_sdk.__version__ import __version__
from stellar_sdk.call_builder.call_builder_async import (
    BaseCallBuilder as BaseCallBuilderAsync,
)
from stellar_sdk.call_builder.call_builder_sync import BaseCallBuilder
from stellar_sdk.client.aiohttp_client import AiohttpClient
from stellar_sdk.client.requests_client import RequestsClient
from stellar_sdk.exceptions import BadRequestError, NotFoundError, NotPageableError
from tests import _horizon_fixtures as hf
from tests.helpers import resolve, take

BuilderFactory = Callable[[str], "BaseCallBuilder | BaseCallBuilderAsync"]


@pytest.fixture(params=["sync", "async"])
async def env(
    request: pytest.FixtureRequest,
) -> AsyncIterator[tuple[BuilderFactory, str]]:
    """A ``(make_builder, client_name)`` pair for each client flavor."""
    if request.param == "sync":
        with RequestsClient() as client:
            yield (
                lambda url: BaseCallBuilder(horizon_url=url, client=client),
                "RequestsClient",
            )
    else:
        async with AiohttpClient() as client:
            yield (
                lambda url: BaseCallBuilderAsync(horizon_url=url, client=client),
                "AiohttpClient",
            )


class TestBaseCallBuilder:
    async def test_get_data(self, env, httpbin_url):
        make_builder, client_name = env
        url = httpbin_url + "get"
        resp = await resolve(
            make_builder(url).limit(10).cursor(10086).order(desc=True).call()
        )
        assert resp["args"] == {"cursor": "10086", "limit": "10", "order": "desc"}
        assert (
            resp["headers"]["User-Agent"]
            == f"py-stellar-base/{__version__}/{client_name}"
        )
        assert resp["headers"]["X-Client-Name"] == "py-stellar-base"
        assert resp["headers"]["X-Client-Version"] == __version__
        assert resp["url"] == httpbin_url + "get?limit=10&cursor=10086&order=desc"

    async def test_stream_data(self, env, horizon_mock):
        make_builder, _ = env
        url = horizon_mock.url + "ledgers"
        horizon_mock.expect(
            "/ledgers", body=hf.stream_body(), content_type="text/event-stream"
        )
        stream = make_builder(url).cursor("now")._stream()
        try:
            messages = await take(stream, 2)
            assert len(messages) == 2
            assert all(isinstance(message, dict) for message in messages)
        finally:
            if isinstance(stream, AsyncGenerator):
                await stream.aclose()
            else:
                stream.close()

    async def test_status_400_raise(self, env, horizon_mock):
        make_builder, _ = env
        url = horizon_mock.url + "accounts/BADACCOUNTID"
        horizon_mock.expect("/accounts/BADACCOUNTID", json=hf.BAD_REQUEST, status=400)
        with pytest.raises(BadRequestError) as err:
            await resolve(make_builder(url).call())

        exception = err.value
        assert exception.status == 400
        assert exception.type == "https://stellar.org/horizon-errors/bad_request"
        assert exception.title == "Bad Request"
        assert exception.detail == "The request you sent was invalid in some way."
        assert exception.extras == {
            "invalid_field": "account_id",
            "reason": "Account ID must start with `G` and contain 56 alphanum characters",
        }

    async def test_status_404_raise(self, env, horizon_mock):
        make_builder, _ = env
        url = horizon_mock.url + "not_found"
        horizon_mock.expect("/not_found", json=hf.NOT_FOUND, status=404)
        with pytest.raises(NotFoundError) as err:
            await resolve(make_builder(url).call())

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

    async def test_get_data_no_link(self, env, httpbin_url):
        make_builder, _ = env
        url = httpbin_url + "get"
        call_builder = make_builder(url).limit(10).cursor(10086).order(desc=True)
        await resolve(call_builder.call())
        assert call_builder.next_href is None
        assert call_builder.prev_href is None

    async def test_get_data_not_pageable_raise(self, env, httpbin_url):
        make_builder, _ = env
        url = httpbin_url + "get"
        call_builder = make_builder(url).limit(10).cursor(10086).order(desc=True)
        await resolve(call_builder.call())
        with pytest.raises(NotPageableError, match=r"The next page does not exist."):
            await resolve(call_builder.next())

        with pytest.raises(NotPageableError, match=r"The prev page does not exist."):
            await resolve(call_builder.prev())

    async def test_get_data_page(self, env, horizon_mock):
        make_builder, _ = env
        url = horizon_mock.url + "transactions"
        next_href = horizon_mock.url + "transactions?cursor=next&limit=10&order=desc"
        prev_href = horizon_mock.url + "transactions?cursor=prev&limit=10&order=asc"
        first_page = {
            "_links": {
                "self": {
                    "href": horizon_mock.url
                    + "transactions?cursor=&limit=10&order=desc"
                },
                "next": {"href": next_href},
            }
        }
        next_page = {
            "_links": {
                "self": {"href": next_href},
                "prev": {"href": prev_href},
            }
        }
        prev_page = {"_links": {"self": {"href": prev_href}}}
        call_builder = make_builder(url).limit(10).order(desc=True)
        horizon_mock.expect(
            "/transactions", query_string="limit=10&order=desc", json=first_page
        )
        horizon_mock.expect(
            "/transactions",
            query_string="cursor=next&limit=10&order=desc",
            json=next_page,
        )
        horizon_mock.expect(
            "/transactions",
            query_string="cursor=prev&limit=10&order=asc",
            json=prev_page,
        )
        first_resp = await resolve(call_builder.call())
        assert (
            first_resp["_links"]["self"]["href"]
            == horizon_mock.url + "transactions?cursor=&limit=10&order=desc"
        )

        next_url = first_resp["_links"]["next"]["href"]
        next_url_cursor = next_url.split("cursor=")[1].split("&")[0]

        next_resp = await resolve(call_builder.next())
        assert (
            next_resp["_links"]["self"]["href"]
            == f"{horizon_mock.url}transactions?cursor={next_url_cursor}&limit=10&order=desc"
        )

        prev_url = next_resp["_links"]["prev"]["href"]
        prev_url_cursor = prev_url.split("cursor=")[1].split("&")[0]
        previous_page = await resolve(call_builder.prev())
        assert (
            previous_page["_links"]["self"]["href"]
            == f"{horizon_mock.url}transactions?cursor={prev_url_cursor}&limit=10&order=asc"
        )

    async def test_horizon_url_params(self, env, httpbin_url):
        make_builder, client_name = env
        url = httpbin_url + "get?version=1.2&auth=myPassw0wd"
        resp = await resolve(
            make_builder(url).limit(10).cursor(10086).order(desc=True).call()
        )
        assert resp["args"] == {
            "auth": "myPassw0wd",
            "cursor": "10086",
            "limit": "10",
            "order": "desc",
            "version": "1.2",
        }
        assert (
            resp["headers"]["User-Agent"]
            == f"py-stellar-base/{__version__}/{client_name}"
        )
        assert resp["headers"]["X-Client-Name"] == "py-stellar-base"
        assert resp["headers"]["X-Client-Version"] == __version__
        assert (
            resp["url"]
            == httpbin_url
            + "get?version=1.2&auth=myPassw0wd&limit=10&cursor=10086&order=desc"
        )
