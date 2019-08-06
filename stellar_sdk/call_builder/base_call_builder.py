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

    def __call_sync(self) -> Response:
        url = urljoin(self.horizon_url, self.endpoint)
        return self.client.get(url, self.params)

    async def __call_async(self) -> Response:
        url = urljoin(self.horizon_url, self.endpoint)
        return await self.client.get(url, self.params)

    def stream(self):
        if self.__async:
            return self.__stream_async()
        else:
            return self.__stream_sync()

    async def __stream_async(self):
        url = urljoin(self.horizon_url, self.endpoint)
        stream = self.client.stream(url, self.params)
        while True:
            yield await stream.__anext__()

    def __stream_sync(self):
        url = urljoin(self.horizon_url, self.endpoint)
        return self.client.stream(url, self.params)

    def cursor(self, cursor):
        self._add_query_param("cursor", cursor)
        return self

    def limit(self, limit):
        self._add_query_param("limit", limit)
        return self

    def order(self, desc=True):
        order = "asc"
        if desc:
            order = "desc"
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
