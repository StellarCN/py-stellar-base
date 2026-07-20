import pytest
from pytest_httpserver import HTTPServer

from stellar_sdk.exceptions import ContentSizeLimitExceededError
from stellar_sdk.sep.exceptions import StellarTomlNotFoundError
from stellar_sdk.sep.stellar_toml import (
    STELLAR_TOML_MAX_SIZE,
    _build_request_url,
    fetch_stellar_toml,
    fetch_stellar_toml_async,
)
from tests.helpers import resolve

TOML_CONTENT = """FEDERATION_SERVER="https://federation.example.com"
WEB_AUTH_ENDPOINT="https://stellar-auth.example.com/auth"
SIGNING_KEY="GDSDOGLZALK6V6DUTHNTACGTR3GI3OSVXK6OQCHDLSAGWXQRUBQVI2KM"
NETWORK_PASSPHRASE="Public Global Stellar Network ; September 2015"
"""


@pytest.fixture(params=["sync", "async"])
def fetch_toml(request: pytest.FixtureRequest):
    if request.param == "sync":
        return fetch_stellar_toml
    return fetch_stellar_toml_async


def _local_domain(httpserver: HTTPServer) -> str:
    return f"{httpserver.host}:{httpserver.port}"


class TestStellarToml:
    async def test_get_success(self, fetch_toml, httpserver):
        httpserver.expect_request("/.well-known/stellar.toml").respond_with_data(
            TOML_CONTENT
        )
        toml = await resolve(fetch_toml(_local_domain(httpserver), use_http=True))
        assert toml.get("FEDERATION_SERVER") == "https://federation.example.com"

    async def test_get_not_found(self, fetch_toml, httpserver):
        httpserver.expect_request("/.well-known/stellar.toml").respond_with_data(
            "", status=404
        )
        with pytest.raises(StellarTomlNotFoundError):
            await resolve(fetch_toml(_local_domain(httpserver), use_http=True))

    async def test_content_size_limit_exceeded(self, fetch_toml, httpserver):
        large_content = "a" * (STELLAR_TOML_MAX_SIZE + 1)
        httpserver.expect_request("/.well-known/stellar.toml").respond_with_data(
            large_content
        )
        with pytest.raises(ContentSizeLimitExceededError):
            await resolve(fetch_toml(_local_domain(httpserver), use_http=True))

    def test_build_request_url(self):
        assert (
            _build_request_url("example.com", False)
            == "https://example.com/.well-known/stellar.toml"
        )
        assert (
            _build_request_url("example.com", True)
            == "http://example.com/.well-known/stellar.toml"
        )
