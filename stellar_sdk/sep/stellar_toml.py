"""
SEP: 0001
Title: stellar.toml
Author: stellar.org
Status: Active
Created: 2017-10-30
Updated: 2019-06-12
Version: 2.1.0
"""

from typing import Any, MutableMapping

import toml

from ..client.aiohttp_client import AiohttpClient
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..client.requests_client import RequestsClient
from ..client.response import Response
from .exceptions import StellarTomlNotFoundError

__all__ = ["fetch_stellar_toml", "fetch_stellar_toml_async"]


def fetch_stellar_toml(
    domain: str,
    client: BaseSyncClient = None,
    use_http: bool = False,
) -> MutableMapping[str, Any]:
    """Retrieve the stellar.toml file from a given domain.

    Retrieve the stellar.toml file for information about interacting with
    Stellar's federation protocol for a given Stellar Anchor (specified by a
    domain).

    :param domain: The domain the .toml file is hosted at.
    :param use_http: Specifies whether the request should go over plain HTTP vs HTTPS.
        Note it is recommended that you **always** use HTTPS.
    :param client: Http Client used to send the request.
    :return: The stellar.toml file as an object via :func:`toml.loads`.
    :raises: :exc:`StellarTomlNotFoundError <stellar_sdk.sep.exceptions.StellarTomlNotFoundError>`:
        if the Stellar toml file could not be found.
    """
    if not client:
        client = RequestsClient()
    url = _build_request_url(domain, use_http)
    raw_resp = client.get(url)
    return _handle_raw_response(raw_resp)


async def fetch_stellar_toml_async(
    domain: str,
    client: BaseAsyncClient = None,
    use_http: bool = False,
) -> MutableMapping[str, Any]:
    """Retrieve the stellar.toml file from a given domain.

    Retrieve the stellar.toml file for information about interacting with
    Stellar's federation protocol for a given Stellar Anchor (specified by a
    domain).

    :param domain: The domain the .toml file is hosted at.
    :param use_http: Specifies whether the request should go over plain HTTP vs HTTPS.
        Note it is recommended that you **always** use HTTPS.
    :param client: Http Client used to send the request.
    :return: The stellar.toml file as an object via :func:`toml.loads`.
    :raises: :exc:`StellarTomlNotFoundError <stellar_sdk.sep.exceptions.StellarTomlNotFoundError>`:
        if the Stellar toml file could not be found.
    """

    if not client:
        client = AiohttpClient()
    url = _build_request_url(domain, use_http)
    raw_resp = await client.get(url)
    return _handle_raw_response(raw_resp)


def _handle_raw_response(raw_resp: Response) -> MutableMapping[str, Any]:
    if raw_resp.status_code == 404:
        raise StellarTomlNotFoundError
    resp = raw_resp.text
    return toml.loads(resp)


def _build_request_url(domain: str, use_http: bool = False) -> str:
    toml_link = "/.well-known/stellar.toml"
    protocol = "https://"
    if use_http:
        protocol = "http://"
    url = protocol + domain + toml_link
    return url
