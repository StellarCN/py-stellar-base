from typing import Union, Dict

import requests
from requests import RequestException
from urllib3.exceptions import NewConnectionError

from .base_sync_client import BaseSyncClient
from ..__version__ import __version__
from ..client.response import Response

USER_AGENT = "py-stellar-sdk/%s/SimpleRequestsClient" % __version__
HEADERS = {
    "X-Client-Name": "py-stellar-sdk",
    "X-Client-Version": __version__,
    "User-Agent": USER_AGENT,
}

__all__ = ["SimpleRequestsClient"]


class SimpleRequestsClient(BaseSyncClient):
    def get(self, url: str, params: Dict[str, str] = None) -> Response:
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
        raise NotImplementedError  # pragma: no cover

    def close(self):
        pass
