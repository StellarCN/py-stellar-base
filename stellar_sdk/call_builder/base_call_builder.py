from typing import Union, Coroutine, Any
from urllib.parse import urljoin

from ..exceptions import (
    NotFoundError,
    BadResponseError,
    BadRequestError,
    UnknownRequestError,
)
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..client.response import Response


class BaseCallBuilder:
    """Creates a new :class:`BaseCallBuilder` pointed to server defined by horizon_url.

    This is an **abstract** class. Do not create this object directly, use :class:`stellar_sdk.server.Server` class.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

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
        """Triggers a HTTP request using this builder's current configuration.

        :return: If it is called synchronous, the response will be returned. If
            it is called asynchronously, it will return Coroutine.
        """
        if self.__async:
            return self.__call_async()
        else:
            return self.__call_sync()

    def __call_sync(self) -> Response:
        url = urljoin(self.horizon_url, self.endpoint)
        resp = self.client.get(url, self.params)
        self._raise_request_exception(resp)
        return resp

    async def __call_async(self) -> Response:
        url = urljoin(self.horizon_url, self.endpoint)
        resp = await self.client.get(url, self.params)
        self._raise_request_exception(resp)
        return resp

    def stream(self):
        """Creates an EventSource that listens for incoming messages from the server.

        See `Horizon Response Format <https://www.stellar.org/developers/horizon/reference/responses.html>`_

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`_

        :return: If it is called synchronous, it will return `Generator`, If
            it is called asynchronously, it will return `AsyncGenerator`.
        """
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
        """Sets `cursor` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        See `Paging <https://www.stellar.org/developers/horizon/reference/paging.html>`_

        :param cursor: A cursor is a value that points to a specific location in a collection of resources.
        :return: current CallBuilder instance
        """
        self._add_query_param("cursor", cursor)
        return self

    def limit(self, limit):
        """Sets `limit` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        See `Paging <https://www.stellar.org/developers/horizon/reference/paging.html>`_

        :param limit: Number of records the server should return.
        :return:
        """
        self._add_query_param("limit", limit)
        return self

    def order(self, desc=True):
        """Sets `order` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        :param desc: Sort direction, `True` to get desc sort direction, the default setting is `True`.
        :return: current CallBuilder instance
        """
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

    def _raise_request_exception(self, response):
        status_code = response.status_code
        if status_code == 200:
            pass
        elif status_code == 400:
            raise BadRequestError(response)
        elif status_code == 404:
            raise NotFoundError(response)
        elif 500 <= status_code < 600:
            raise BadResponseError(response)
        else:
            raise UnknownRequestError(response)

    def __eq__(self, other: "BaseCallBuilder"):
        if not isinstance(other, self.__class__):
            return False
        return (
            self.client == other.client
            and self.params == other.params
            and self.endpoint == other.endpoint
            and self.horizon_url == other.horizon_url
        )
