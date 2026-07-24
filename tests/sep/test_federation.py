import re
from typing import Any, NamedTuple

import pytest
from pytest_httpserver import HTTPServer

from stellar_sdk.exceptions import ContentSizeLimitExceededError
from stellar_sdk.sep.exceptions import (
    BadFederationResponseError,
    FederationServerNotFoundError,
    InvalidFederationAddress,
)
from stellar_sdk.sep.federation import (
    FEDERATION_RESPONSE_MAX_SIZE,
    FederationRecord,
    _split_stellar_address,
    resolve_account_id,
    resolve_account_id_async,
    resolve_stellar_address,
    resolve_stellar_address_async,
)
from tests.helpers import resolve

ACCOUNT_ID = "GAWCQ74PIJO2NH6F3KZ4AMX27UAKBXWC7KG3FLYJOFIMRQF3RSZHCOVN"


class FederationApi(NamedTuple):
    resolve_stellar_address: Any
    resolve_account_id: Any


@pytest.fixture(params=["sync", "async"])
async def federation_api(
    request: pytest.FixtureRequest,
    close_internal_aiohttp_clients: None,
) -> FederationApi:
    if request.param == "sync":
        return FederationApi(resolve_stellar_address, resolve_account_id)
    return FederationApi(resolve_stellar_address_async, resolve_account_id_async)


def _local_domain(httpserver: HTTPServer) -> str:
    return f"{httpserver.host}:{httpserver.port}"


def _expect_toml(httpserver: HTTPServer, body: str | None = None) -> None:
    """Serve a stellar.toml whose FEDERATION_SERVER points back at httpserver."""
    if body is None:
        body = f'FEDERATION_SERVER="{httpserver.url_for("/federation")}"\n'
    httpserver.expect_request("/.well-known/stellar.toml").respond_with_data(body)


class TestFederation:
    async def test_resolve_by_stellar_address(self, federation_api, httpserver):
        stellar_address = f"hello*{_local_domain(httpserver)}"
        _expect_toml(httpserver)
        httpserver.expect_request(
            "/federation", query_string={"type": "name", "q": stellar_address}
        ).respond_with_json(
            {
                "account_id": ACCOUNT_ID,
                "memo_type": "text",
                "memo": "Nice to meet you :-)",
            }
        )
        record = await resolve(
            federation_api.resolve_stellar_address(stellar_address, use_http=True)
        )
        assert record == FederationRecord(
            stellar_address=stellar_address,
            account_id=ACCOUNT_ID,
            memo_type="text",
            memo="Nice to meet you :-)",
        )

    async def test_resolve_by_stellar_address_federation_not_found(
        self, federation_api, httpserver
    ):
        stellar_address = f"hello*{_local_domain(httpserver)}"
        _expect_toml(httpserver, body="")
        with pytest.raises(
            FederationServerNotFoundError,
            match=rf"Unable to find federation server at {re.escape(_local_domain(httpserver))}\.",
        ):
            await resolve(
                federation_api.resolve_stellar_address(stellar_address, use_http=True)
            )

    async def test_resolve_by_stellar_address_with_federation_url(
        self, federation_api, httpserver
    ):
        stellar_address = f"hello*{_local_domain(httpserver)}"
        httpserver.expect_request(
            "/federation", query_string={"type": "name", "q": stellar_address}
        ).respond_with_json(
            {
                "account_id": ACCOUNT_ID,
                "memo_type": "text",
                "memo": "Nice to meet you :-)",
            }
        )
        record = await resolve(
            federation_api.resolve_stellar_address(
                stellar_address, federation_url=httpserver.url_for("/federation")
            )
        )
        assert record.account_id == ACCOUNT_ID

    async def test_resolve_by_account_id_with_domain(self, federation_api, httpserver):
        stellar_address = f"hello*{_local_domain(httpserver)}"
        _expect_toml(httpserver)
        httpserver.expect_request(
            "/federation", query_string={"type": "id", "q": ACCOUNT_ID}
        ).respond_with_json(
            {
                "stellar_address": stellar_address,
                "memo_type": "text",
                "memo": "Nice to meet you :-)",
            }
        )
        record = await resolve(
            federation_api.resolve_account_id(
                ACCOUNT_ID, domain=_local_domain(httpserver), use_http=True
            )
        )
        assert record == FederationRecord(
            stellar_address=stellar_address,
            account_id=ACCOUNT_ID,
            memo_type="text",
            memo="Nice to meet you :-)",
        )

    async def test_resolve_by_account_id_without_domain_and_federation_url(
        self, federation_api
    ):
        with pytest.raises(
            ValueError, match=r"You should provide either `domain` or `federation_url`."
        ):
            await resolve(federation_api.resolve_account_id(ACCOUNT_ID))

    async def test_resolve_by_account_id_federation_not_found(
        self, federation_api, httpserver
    ):
        _expect_toml(httpserver, body="")
        with pytest.raises(
            FederationServerNotFoundError,
            match=rf"Unable to find federation server at {re.escape(_local_domain(httpserver))}\.",
        ):
            await resolve(
                federation_api.resolve_account_id(
                    ACCOUNT_ID, domain=_local_domain(httpserver), use_http=True
                )
            )

    async def test_not_found_record_at_federation(self, federation_api, httpserver):
        stellar_address = f"hello*{_local_domain(httpserver)}"
        _expect_toml(httpserver)
        httpserver.expect_request(
            "/federation", query_string={"type": "name", "q": stellar_address}
        ).respond_with_data("", status=404)
        with pytest.raises(BadFederationResponseError) as err:
            await resolve(
                federation_api.resolve_stellar_address(stellar_address, use_http=True)
            )
        assert err.value.status == 404

    async def test_federation_response_size_limit_exceeded(
        self, federation_api, httpserver
    ):
        stellar_address = f"hello*{_local_domain(httpserver)}"
        large_content = "x" * (FEDERATION_RESPONSE_MAX_SIZE + 1)
        _expect_toml(httpserver)
        httpserver.expect_request(
            "/federation", query_string={"type": "name", "q": stellar_address}
        ).respond_with_data(large_content)
        with pytest.raises(ContentSizeLimitExceededError):
            await resolve(
                federation_api.resolve_stellar_address(stellar_address, use_http=True)
            )

    def test_split_address(self):
        assert _split_stellar_address("hello*example.com") == {
            "name": "hello",
            "domain": "example.com",
        }

    @pytest.mark.parametrize("stellar_address", ["", "hey", "hey*hello*overcat.me"])
    def test_split_invalid_address(self, stellar_address):
        with pytest.raises(InvalidFederationAddress):
            _split_stellar_address(stellar_address)
