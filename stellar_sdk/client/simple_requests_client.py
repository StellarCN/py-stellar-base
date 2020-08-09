from typing import Union, Dict

import requests
from requests import RequestException
from urllib3.exceptions import NewConnectionError

from .base_sync_client import BaseSyncClient
from ..__version__ import __version__
from ..client.response import Response

USER_AGENT = f"py-stellar-sdk/{__version__}/SimpleRequestsClient"
HEADERS = {
    "X-Client-Name": "py-stellar-sdk",
    "X-Client-Version": __version__,
    "User-Agent": USER_AGENT,
}

__all__ = ["SimpleRequestsClient"]


class SimpleRequestsClient(BaseSyncClient):
    """The :class:`SimpleRequestsClient` object is a synchronous http client,
    which represents the interface for making requests to a server instance.

    **This client is to guide you in writing a client that suits your needs.
    I don't recommend that you actually use it.**
    """

    def get(self, url: str, params: Dict[str, str] = None) -> Response:
        """Perform HTTP GET request.

        :param url: the request url
        :param params: the request params
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        try:
            resp = requests.get(url=url, params=params, headers=HEADERS)
        except (RequestException, NewConnectionError) as err:
            raise ConnectionError(err)
        return Response(
            status_code=resp.status_code,
            text=resp.text,
            headers=dict(resp.headers),
            url=resp.url,
        )

    def post(self, url: str, data: Dict[str, str]) -> Response:
        """Perform HTTP POST request.

        :param url: the request url
        :param data: the data send to server
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        try:
            resp = requests.post(url=url, data=data, headers=HEADERS)
        except (RequestException, NewConnectionError) as err:
            raise ConnectionError(err)
        return Response(
            status_code=resp.status_code,
            text=resp.text,
            headers=dict(resp.headers),
            url=resp.url,
        )

    def stream(
        self, url: str, params: Dict[str, str] = None
    ) -> None:  # Here should return NoReturn, but it has not been implemented in PyPy.
        """
        **Not Implemented**

        :param url: the request url
        :param params: the request params
        :return: None
        """
        raise NotImplementedError  # pragma: no cover

    def close(self):
        pass  # pragma: no cover
