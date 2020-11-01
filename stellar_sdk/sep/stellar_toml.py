"""
SEP: 0001
Title: stellar.toml
Author: stellar.org
Status: Active
Created: 2017-10-30
Updated: 2019-06-12
Version: 2.1.0
"""
from typing import Union, Any, Coroutine, Dict

import toml

from .exceptions import StellarTomlNotFoundError
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..client.requests_client import RequestsClient
from ..client.response import Response


def fetch_stellar_toml(
    domain: str,
    client: Union[BaseAsyncClient, BaseSyncClient] = None,
    use_http: bool = False,
) -> Union[Coroutine[Any, Any, Dict[str, Any]], Dict[str, Any]]:
    """Retrieve the stellar.toml file from a given domain.

    Retrieve the stellar.toml file for information about interacting with
    Stellar's federation protocol for a given Stellar Anchor (specified by a
    domain).

    :param domain: The domain the .toml file is hosted at.
    :param use_http: Specifies whether the request should go over plain HTTP vs HTTPS.
        Note it is recommend that you *always* use HTTPS.
    :param client: Http Client used to send the request.
    :return: The stellar.toml file as a an object via :func:`toml.loads`.
    :raises: :exc:`StellarTomlNotFoundError <stellar_sdk.sep.exceptions.StellarTomlNotFoundError>`:
        if the Stellar toml file could not not be found.
    """
    if not client:
        client = RequestsClient()

    toml_link = "/.well-known/stellar.toml"
    protocol = "https://"
    if use_http:
        protocol = "http://"
    url = protocol + domain + toml_link

    if isinstance(client, BaseAsyncClient):
        return __fetch_async(url, client)
    elif isinstance(client, BaseSyncClient):
        return __fetch_sync(url, client)
    else:
        raise TypeError(
            "This `client` class should be an instance "
            "of `stellar_sdk.client.base_async_client.BaseAsyncClient` "
            "or `stellar_sdk.client.base_sync_client.BaseSyncClient`."
        )


async def __fetch_async(url: str, client: BaseAsyncClient) -> Dict[str, Any]:
    raw_resp = await client.get(url)
    return __handle_raw_response(raw_resp)


def __fetch_sync(url: str, client: BaseSyncClient) -> Dict[str, Any]:
    raw_resp = client.get(url)
    return __handle_raw_response(raw_resp)


def __handle_raw_response(raw_resp: Response) -> Dict[str, Any]:
    if raw_resp.status_code == 404:
        raise StellarTomlNotFoundError
    resp = raw_resp.text
    return toml.loads(resp)  # type: ignore[return-value]
