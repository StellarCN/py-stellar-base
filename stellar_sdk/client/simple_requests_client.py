from typing import NoReturn

import requests

from .base_sync_client import BaseSyncClient
from ..__version__ import __version__
from ..client.response import Response

USER_AGENT = "py-stellar-sdk/%s/SimpleRequestsClient" % __version__
HEADERS = {
    "X-Client-Name": "py-stellar-sdk",
    "X-Client-Version": __version__,
    "User-Agent": USER_AGENT,
}


class SimpleRequestsClient(BaseSyncClient):
    def get(self, url: str, params: dict) -> Response:
        resp = requests.get(url=url, params=params, headers=HEADERS)
        return Response(
            status_code=resp.status_code,
            text=resp.text,
            headers=dict(resp.headers),
            url=resp.url,
        )

    def post(self, url: str, data: dict) -> Response:
        resp = requests.post(url=url, data=data, headers=HEADERS)
        return Response(
            status_code=resp.status_code,
            text=resp.text,
            headers=dict(resp.headers),
            url=resp.url,
        )

    def stream(self, url: str, params: dict) -> NoReturn:
        raise NotImplementedError  # pragma: no cover

    def close(self):
        pass
