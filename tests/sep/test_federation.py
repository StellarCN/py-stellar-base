import asyncio

import pytest
import requests_mock
from aioresponses import aioresponses

from stellar_sdk.client.aiohttp_client import AiohttpClient
from stellar_sdk.sep.exceptions import (
    BadFederationResponseError,
    FederationServerNotFoundError,
    InvalidFederationAddress,
)
from stellar_sdk.sep.federation import (
    FederationRecord,
    _split_stellar_address,
    resolve_account_id,
    resolve_account_id_async,
    resolve_stellar_address,
    resolve_stellar_address_async,
)


class TestFederation:
    ACCOUNT_ID = "GAWCQ74PIJO2NH6F3KZ4AMX27UAKBXWC7KG3FLYJOFIMRQF3RSZHCOVN"
    STELLAR_ADDRESS = "hello*example.com"
    DOMAIN = "example.com"
    FEDERATION_SERVER = "https://federation.example.com"
    FEDERATION_RECORD = FederationRecord(
        stellar_address=STELLAR_ADDRESS,
        account_id=ACCOUNT_ID,
        memo_type="text",
        memo="Nice to meet you :-)",
    )
    TOML_CONTENT = """FEDERATION_SERVER="https://federation.example.com"
    WEB_AUTH_ENDPOINT="https://stellar-auth.example.com/auth"
    SIGNING_KEY="GDSDOGLZALK6V6DUTHNTACGTR3GI3OSVXK6OQCHDLSAGWXQRUBQVI2KM"
    NETWORK_PASSPHRASE="Public Global Stellar Network ; September 2015"
    """

    def test_resolve_by_stellar_address_sync(self):
        with requests_mock.Mocker() as m:
            m.get(
                "https://example.com/.well-known/stellar.toml", text=self.TOML_CONTENT
            )
            m.get(
                "https://federation.example.com/?type=name&q=hello%2Aexample.com",
                json={
                    "account_id": self.ACCOUNT_ID,
                    "memo_type": "text",
                    "memo": "Nice to meet you :-)",
                },
            )
            record = resolve_stellar_address(self.STELLAR_ADDRESS)
            assert record == self.FEDERATION_RECORD

    def test_resolve_by_stellar_address_async(self):
        loop = asyncio.get_event_loop()
        with aioresponses() as m:
            m.get(
                "https://example.com/.well-known/stellar.toml", body=self.TOML_CONTENT
            )
            m.get(
                "https://federation.example.com/?type=name&q=hello%2Aexample.com",
                payload={
                    "account_id": self.ACCOUNT_ID,
                    "memo_type": "text",
                    "memo": "Nice to meet you :-)",
                },
            )
            record = loop.run_until_complete(
                resolve_stellar_address_async(self.STELLAR_ADDRESS)
            )
            assert record == self.FEDERATION_RECORD

    def test_resolve_by_stellar_address_federation_not_found_sync(self):
        with requests_mock.Mocker() as m:
            m.get("https://example.com/.well-known/stellar.toml", text="")
            with pytest.raises(
                FederationServerNotFoundError,
                match="Unable to find federation server at example.com",
            ):
                resolve_stellar_address(self.STELLAR_ADDRESS)

    def test_resolve_by_stellar_address_federation_not_found_async(self):
        loop = asyncio.get_event_loop()
        with aioresponses() as m:
            m.get("https://example.com/.well-known/stellar.toml", body="")
            with pytest.raises(
                FederationServerNotFoundError,
                match="Unable to find federation server at example.com.",
            ):
                loop.run_until_complete(
                    resolve_stellar_address_async(
                        self.STELLAR_ADDRESS, client=AiohttpClient()
                    )
                )

    def test_resolve_by_stellar_address_with_federation_url_sync(self):
        with requests_mock.Mocker() as m:
            m.get(
                "https://federation.example.com/?type=name&q=hello%2Aexample.com",
                json={
                    "account_id": self.ACCOUNT_ID,
                    "memo_type": "text",
                    "memo": "Nice to meet you :-)",
                },
            )

            record = resolve_stellar_address(
                "hello*example.com", federation_url=self.FEDERATION_SERVER
            )
            assert record.account_id == self.ACCOUNT_ID

    def test_resolve_by_stellar_address_with_federation_url_async(self):
        loop = asyncio.get_event_loop()
        with aioresponses() as m:
            m.get(
                "https://example.com/.well-known/stellar.toml", body=self.TOML_CONTENT
            )
            m.get(
                "https://federation.example.com/?type=name&q=hello%2Aexample.com",
                payload={
                    "account_id": self.ACCOUNT_ID,
                    "memo_type": "text",
                    "memo": "Nice to meet you :-)",
                },
            )
            record = loop.run_until_complete(
                resolve_stellar_address_async(
                    "hello*example.com", federation_url=self.FEDERATION_SERVER
                )
            )
            assert record.account_id == self.ACCOUNT_ID

    def test_resolve_by_account_id_with_domain_sync(self):
        with requests_mock.Mocker() as m:
            m.get(
                "https://example.com/.well-known/stellar.toml", text=self.TOML_CONTENT
            )
            m.get(
                "https://federation.example.com/?type=id&q=GAWCQ74PIJO2NH6F3KZ4AMX27UAKBXWC7KG3FLYJOFIMRQF3RSZHCOVN",
                json={
                    "stellar_address": "hello*example.com",
                    "memo_type": "text",
                    "memo": "Nice to meet you :-)",
                },
            )
            record = resolve_account_id(self.ACCOUNT_ID, domain=self.DOMAIN)
            assert record == self.FEDERATION_RECORD

    def test_resolve_by_account_id_with_domain_async(self):
        loop = asyncio.get_event_loop()
        with aioresponses() as m:
            m.get(
                "https://example.com/.well-known/stellar.toml", body=self.TOML_CONTENT
            )
            m.get(
                "https://federation.example.com/?type=id&q=GAWCQ74PIJO2NH6F3KZ4AMX27UAKBXWC7KG3FLYJOFIMRQF3RSZHCOVN",
                payload={
                    "stellar_address": "hello*example.com",
                    "memo_type": "text",
                    "memo": "Nice to meet you :-)",
                },
            )
            record = loop.run_until_complete(
                resolve_account_id_async(self.ACCOUNT_ID, domain=self.DOMAIN)
            )
            assert record == self.FEDERATION_RECORD

    def test_resolve_by_account_id_without_domain_and_federation_url(self):
        with pytest.raises(
            ValueError, match="You should provide either `domain` or `federation_url`."
        ):
            resolve_account_id(self.ACCOUNT_ID)

    def test_resolve_by_account_id_federation_not_found_sync(self):
        with requests_mock.Mocker() as m:
            m.get("https://example.com/.well-known/stellar.toml", text="")
            with pytest.raises(
                FederationServerNotFoundError,
                match="Unable to find federation server at example.com.",
            ):
                resolve_account_id(self.ACCOUNT_ID, domain="example.com")

    def test_resolve_by_account_id_federation_not_found_async(self):
        loop = asyncio.get_event_loop()
        with aioresponses() as m:
            m.get("https://example.com/.well-known/stellar.toml", body="")
            with pytest.raises(
                FederationServerNotFoundError,
                match="Unable to find federation server at example.com.",
            ):
                loop.run_until_complete(
                    resolve_account_id_async(
                        self.ACCOUNT_ID, domain="example.com", client=AiohttpClient()
                    )
                )

    def test_not_found_record_at_federation(self):
        with pytest.raises(BadFederationResponseError) as err:
            with requests_mock.Mocker() as m:
                m.get(
                    "https://example.com/.well-known/stellar.toml",
                    text=self.TOML_CONTENT,
                )
                m.get(
                    "https://federation.example.com/?type=name&q=hello%2Aexample.com",
                    status_code=404,
                )
                record = resolve_stellar_address(self.STELLAR_ADDRESS)
                assert record == self.FEDERATION_RECORD
        assert err.value.status == 404

    def test_split_address(self):
        assert _split_stellar_address(self.STELLAR_ADDRESS) == {
            "name": "hello",
            "domain": "example.com",
        }

    @pytest.mark.parametrize("stellar_address", ["", "hey", "hey*hello*overcat.me"])
    def test_split_invalid_address(self, stellar_address):
        with pytest.raises(InvalidFederationAddress):
            _split_stellar_address(stellar_address)
