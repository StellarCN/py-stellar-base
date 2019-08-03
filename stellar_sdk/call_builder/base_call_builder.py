from urllib.parse import urljoin

from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..client.response import Response


class BaseCallBuilder:
    def __init__(self, horizon_url, client):
        if isinstance(client, BaseAsyncClient):
            self.__async = True
        elif isinstance(client, BaseSyncClient):
            self.__async = False

        self.client = client
        self.horizon_url = horizon_url
        self.filter = []
        self.params = {}
        self.endpoint = ""

    def call(self) -> Response:
        if self.__async:
            return self.__call_async()
        else:
            return self.__call_sync()

    async def __call_async(self) -> Response:
        url = urljoin(self.horizon_url, self.endpoint)
        params = self.__query_params(**self.params)
        return await self.client.get(url, params)

    async def stream_async(self):
        url = urljoin(self.horizon_url, self.endpoint)
        stream = self.client.stream(url)
        while True:
            yield await stream.__anext__()

    def __call_sync(self) -> Response:
        url = urljoin(self.horizon_url, self.endpoint)
        params = self.__query_params(**self.params)
        return self.client.get(url, params)

    def stream_sync(self):
        pass

    def cursor(self, cursor):
        self.params["cursor"] = cursor
        return self

    def limit(self, limit):
        self.params["limit"] = limit
        return self

    def order(self, order):
        self.params["order"] = order
        return self
    
    def __query_params(self, **kwargs):
        params = {}
        for k, v in kwargs.items():
            if v is None:
                pass
            elif v is True:
                params[k] = "true"
            elif v is False:
                params[k] = "false"
            else:
                params[k] = v
        return params
