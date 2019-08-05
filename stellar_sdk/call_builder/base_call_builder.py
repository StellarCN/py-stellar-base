from typing import Union, Coroutine, Any, AsyncGenerator
from urllib.parse import urljoin

from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..client.response import Response


class BaseCallBuilder:
    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        if isinstance(client, BaseAsyncClient):
            self.__async = True
        elif isinstance(client, BaseSyncClient):
            self.__async = False

        self.client = client
        self.horizon_url = horizon_url
        self.params = {}
        self.endpoint = ""

    def call(self) -> Union[Response, Coroutine[Any, Any, Response]]:
        if self.__async:
            return self.__call_async()
        else:
            return self.__call_sync()

    async def __call_async(self) -> Response:
        url = urljoin(self.horizon_url, self.endpoint)
        return await self.client.get(url, self.params)

    async def stream_async(self):
        url = urljoin(self.horizon_url, self.endpoint)
        stream = self.client.stream(url)
        while True:
            yield await stream.__anext__()

    def __call_sync(self) -> Response:
        url = urljoin(self.horizon_url, self.endpoint)
        return self.client.get(url, self.params)

    def stream_sync(self):
        pass

    def cursor(self, cursor):
        self._add_query_param("cursor", cursor)
        return self

    def limit(self, limit):
        self._add_query_param("limit", limit)
        return self

    def order(self, order):
        self._add_query_param("order", order)
        return self

    def _add_query_param(self, key, value):
        if value is None:
            pass
        elif value is True:
            self.params[key] = "true"
        else:
            self.params[key] = value

    def _add_query_params(self, params: dict):
        for k, v in params.items():
            self._add_query_param(k, v)
