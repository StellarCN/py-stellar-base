import requests

from .base_sync_client import BaseSyncClient
from ..client.response import Response


class SimpleRequestsClient(BaseSyncClient):
    def get(self, url, params) -> Response:
        resp = requests.get(url, params)
        return Response(status_code=resp.status_code, text=resp.text, headers=dict(resp.headers), url=resp.url)

    def post(self, url, params) -> Response:
        resp = requests.post(url, params)
        return Response(status_code=resp.status_code, text=resp.text, headers=dict(resp.headers), url=resp.url)

    def stream(self, url):
        raise NotImplementedError
