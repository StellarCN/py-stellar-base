"""
SEP: 0002
Title: Federation protocol
Author: stellar.org
Status: Final
Created: 2017-10-30
Updated: 2019-10-10
Version 1.1.0
"""

from typing import Dict, Optional

from ..client.aiohttp_client import AiohttpClient
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..client.requests_client import RequestsClient
from ..client.response import Response
from .exceptions import (
    BadFederationResponseError,
    FederationServerNotFoundError,
    InvalidFederationAddress,
)
from .stellar_toml import fetch_stellar_toml, fetch_stellar_toml_async

SEPARATOR = "*"
FEDERATION_SERVER_KEY = "FEDERATION_SERVER"

__all__ = [
    "FederationRecord",
    "resolve_stellar_address",
    "resolve_stellar_address_async",
    "resolve_account_id",
    "resolve_account_id_async",
]


class FederationRecord:
    def __init__(
        self,
        account_id: str,
        stellar_address: str,
        memo_type: Optional[str],
        memo: Optional[str],
    ) -> None:
        """The :class:`FederationRecord`, which represents record in federation server.

        :param account_id: Stellar public key / account ID
        :param stellar_address: Stellar address
        :param memo_type: Type of memo to attach to transaction, one of ``text``, ``id`` or ``hash``
        :param memo: value of memo to attach to transaction, for ``hash`` this should be base64-encoded.
            This field should always be of type ``string`` (even when `memo_type` is equal ``id``) to support parsing
            value in languages that don't support big numbers.
        """
        self.account_id: str = account_id
        self.stellar_address: str = stellar_address
        self.memo_type: Optional[str] = memo_type
        self.memo: Optional[str] = memo

    def __hash__(self):
        return hash((self.account_id, self.stellar_address, self.memo_type, self.memo))

    def __repr__(self):
        return (
            f"<FederationRecord [account_id={self.account_id}, stellar_address={self.stellar_address}, "
            f"memo_type={self.memo_type}, memo={self.memo}]>"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.account_id == other.account_id
            and self.stellar_address == other.stellar_address
            and self.memo_type == other.memo_type
            and self.memo == other.memo
        )


def resolve_stellar_address(
    stellar_address: str,
    client: BaseSyncClient = None,
    federation_url: str = None,
    use_http: bool = False,
) -> FederationRecord:
    """Get the federation record if the user was found for a given Stellar address.

    :param stellar_address: address Stellar address (ex. ``"bob*stellar.org"``).
    :param client: Http Client used to send the request.
    :param federation_url: The federation server URL (ex. ``"https://stellar.org/federation"``),
        if you don't set this value, we will try to get it from `stellar_address`.
    :param use_http: Specifies whether the request should go over plain HTTP vs HTTPS.
        Note it is recommended that you **always** use HTTPS.
    :return: Federation record.
    """
    if not client:
        client = RequestsClient()
    parts = _split_stellar_address(stellar_address)
    domain = parts["domain"]
    if federation_url is None:
        federation_url = fetch_stellar_toml(domain, use_http=use_http).get(  # type: ignore[union-attr]
            FEDERATION_SERVER_KEY
        )
    if federation_url is None:
        raise FederationServerNotFoundError(
            f"Unable to find federation server at {domain}."
        )
    raw_resp = client.get(federation_url, {"type": "name", "q": stellar_address})
    return _handle_raw_response(raw_resp, stellar_address=stellar_address)


async def resolve_stellar_address_async(
    stellar_address: str,
    client: BaseAsyncClient = None,
    federation_url: str = None,
    use_http: bool = False,
) -> FederationRecord:
    """Get the federation record if the user was found for a given Stellar address.

    :param stellar_address: address Stellar address (ex. ``"bob*stellar.org"``).
    :param client: Http Client used to send the request.
    :param federation_url: The federation server URL (ex. ``"https://stellar.org/federation"``),
        if you don't set this value, we will try to get it from `stellar_address`.
    :param use_http: Specifies whether the request should go over plain HTTP vs HTTPS.
        Note it is recommended that you **always** use HTTPS.
    :return: Federation record.
    """
    if not client:
        client = AiohttpClient()
    parts = _split_stellar_address(stellar_address)
    domain = parts["domain"]
    if federation_url is None:
        federation_url = (
            await fetch_stellar_toml_async(domain, client=client, use_http=use_http)
        ).get(FEDERATION_SERVER_KEY)
    if federation_url is None:
        raise FederationServerNotFoundError(
            f"Unable to find federation server at {domain}."
        )
    raw_resp = await client.get(federation_url, {"type": "name", "q": stellar_address})
    return _handle_raw_response(raw_resp, stellar_address=stellar_address)


def resolve_account_id(
    account_id: str,
    domain: str = None,
    federation_url: str = None,
    client: BaseSyncClient = None,
    use_http: bool = False,
) -> FederationRecord:
    """Given an account ID, get their federation record if the user was found

    :param account_id: Account ID (ex. ``"GBYNR2QJXLBCBTRN44MRORCMI4YO7FZPFBCNOKTOBCAAFC7KC3LNPRYS"``)
    :param domain: Get `federation_url` from the domain, you don't need to set this value if `federation_url` is set.
    :param federation_url: The federation server URL (ex. ``"https://stellar.org/federation"``).
    :param client: Http Client used to send the request.
    :param use_http: Specifies whether the request should go over plain HTTP vs HTTPS.
        Note it is recommended that you **always** use HTTPS.
    :return: Federation record.
    """
    if domain is None and federation_url is None:
        raise ValueError("You should provide either `domain` or `federation_url`.")

    if not client:
        client = RequestsClient()
    if domain is not None:
        federation_url = fetch_stellar_toml(domain, client, use_http).get(  # type: ignore[union-attr]
            FEDERATION_SERVER_KEY
        )
        if federation_url is None:
            raise FederationServerNotFoundError(
                f"Unable to find federation server at {domain}."
            )
    assert federation_url is not None
    raw_resp = client.get(federation_url, {"type": "id", "q": account_id})
    return _handle_raw_response(raw_resp, account_id=account_id)


async def resolve_account_id_async(
    account_id: str,
    domain: str = None,
    federation_url: str = None,
    client: BaseAsyncClient = None,
    use_http: bool = False,
) -> FederationRecord:
    """Given an account ID, get their federation record if the user was found

    :param account_id: Account ID (ex. ``"GBYNR2QJXLBCBTRN44MRORCMI4YO7FZPFBCNOKTOBCAAFC7KC3LNPRYS"``)
    :param domain: Get `federation_url` from the domain, you don't need to set this value if `federation_url` is set.
    :param federation_url: The federation server URL (ex. ``"https://stellar.org/federation"``).
    :param client: Http Client used to send the request.
    :param use_http: Specifies whether the request should go over plain HTTP vs HTTPS.
        Note it is recommended that you **always** use HTTPS.
    :return: Federation record.
    """
    if domain is None and federation_url is None:
        raise ValueError("You should provide either `domain` or `federation_url`.")

    if not client:
        client = AiohttpClient()
    if domain is not None:
        federation_url = (await fetch_stellar_toml_async(domain, client, use_http)).get(
            FEDERATION_SERVER_KEY
        )
        if federation_url is None:
            raise FederationServerNotFoundError(
                f"Unable to find federation server at {domain}."
            )
    assert federation_url is not None
    raw_resp = await client.get(federation_url, {"type": "id", "q": account_id})
    return _handle_raw_response(raw_resp, account_id=account_id)


def _handle_raw_response(
    raw_resp: Response, stellar_address=None, account_id=None
) -> FederationRecord:
    if not 200 <= raw_resp.status_code < 300:
        raise BadFederationResponseError(raw_resp)
    data = raw_resp.json()
    account_id = account_id or data.get("account_id")
    stellar_address = stellar_address or data.get("stellar_address")
    memo_type = data.get("memo_type")
    memo = data.get("memo")
    return FederationRecord(
        account_id=account_id,
        stellar_address=stellar_address,
        memo_type=memo_type,
        memo=memo,
    )


def _split_stellar_address(address: str) -> Dict[str, str]:
    parts = address.split(SEPARATOR)
    if len(parts) != 2:
        raise InvalidFederationAddress(
            "Address should be a valid address, such as `bob*stellar.org`"
        )
    name, domain = parts
    return {"name": name, "domain": domain}
