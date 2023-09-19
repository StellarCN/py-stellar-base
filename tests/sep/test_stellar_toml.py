import asyncio

import pytest
import requests_mock
from aioresponses import aioresponses

from stellar_sdk.sep.exceptions import StellarTomlNotFoundError
from stellar_sdk.sep.stellar_toml import fetch_stellar_toml, fetch_stellar_toml_async


class TestStellarToml:
    TOML_CONTENT = """FEDERATION_SERVER="https://federation.example.com"
WEB_AUTH_ENDPOINT="https://stellar-auth.example.com/auth"
SIGNING_KEY="GDSDOGLZALK6V6DUTHNTACGTR3GI3OSVXK6OQCHDLSAGWXQRUBQVI2KM"
NETWORK_PASSPHRASE="Public Global Stellar Network ; September 2015"
"""

    def test_get_success_sync(self):
        with requests_mock.Mocker() as m:
            m.get(
                "https://example.com/.well-known/stellar.toml", text=self.TOML_CONTENT
            )
            toml = fetch_stellar_toml("example.com", None)
            assert toml.get("FEDERATION_SERVER") == "https://federation.example.com"

    def test_get_success_async(self):
        loop = asyncio.get_event_loop()
        with aioresponses() as m:
            m.get(
                "https://example.com/.well-known/stellar.toml", body=self.TOML_CONTENT
            )
            toml = loop.run_until_complete(fetch_stellar_toml_async("example.com"))
            assert toml.get("FEDERATION_SERVER") == "https://federation.example.com"

    def test_get_success_http(self):
        with requests_mock.Mocker() as m:
            m.get("http://example.com/.well-known/stellar.toml", text=self.TOML_CONTENT)
            toml = fetch_stellar_toml("example.com", None, True)
            assert toml.get("FEDERATION_SERVER") == "https://federation.example.com"

    def test_get_not_found(self):
        with requests_mock.Mocker() as mocker:
            mocker.register_uri(
                "GET", "https://example.com/.well-known/stellar.toml", status_code=404
            )
            with pytest.raises(StellarTomlNotFoundError):
                fetch_stellar_toml("example.com")
