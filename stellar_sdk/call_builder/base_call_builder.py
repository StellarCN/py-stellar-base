from typing import (
    Union,
    Coroutine,
    Any,
    Dict,
    Mapping,
    Generator,
    AsyncGenerator,
    Optional,
)

from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..exceptions import raise_request_exception, NotPageableError
from ..utils import urljoin_with_query


class BaseCallBuilder:
    """Creates a new :class:`BaseCallBuilder` pointed to server defined by horizon_url.

    This is an **abstract** class. Do not create this object directly, use :class:`stellar_sdk.server.Server` class.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:

        self.__async: bool = False
        if isinstance(client, BaseAsyncClient):
            self.__async = True

        self.client: Union[BaseAsyncClient, BaseSyncClient] = client
        self.horizon_url: str = horizon_url
        self.params: Dict[str, str] = {}
        self.endpoint: str = ""
        self.prev_href: Optional[str] = None
        self.next_href: Optional[str] = None

    def call(self) -> Union[Dict[str, Any], Coroutine[Any, Any, Dict[str, Any]]]:
        """Triggers a HTTP request using this builder's current configuration.

        :return: If it is called synchronous, the response will be returned. If
            it is called asynchronously, it will return Coroutine.
        :raises:
            | :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`: if you have not successfully
                connected to the server.
            | :exc:`NotFoundError <stellar_sdk.exceptions.NotFoundError>`: if status_code == 404
            | :exc:`BadRequestError <stellar_sdk.exceptions.BadRequestError>`: if 400 <= status_code < 500
                and status_code != 404
            | :exc:`BadResponseError <stellar_sdk.exceptions.BadResponseError>`: if 500 <= status_code < 600
            | :exc:`UnknownRequestError <stellar_sdk.exceptions.UnknownRequestError>`: if an unknown error occurs,
                please submit an issue
        """
        url = urljoin_with_query(self.horizon_url, self.endpoint)
        return self.__call(url, self.params)

    def __call(self, url: str, params: dict = None):
        if self.__async:
            return self.__call_async(url, params)
        else:
            return self.__call_sync(url, params)

    def __call_sync(self, url: str, params: dict = None) -> Dict[str, Any]:
        raw_resp = self.client.get(url, params)
        raise_request_exception(raw_resp)
        resp = raw_resp.json()
        self._check_pageable(resp)
        return resp

    async def __call_async(self, url: str, params: dict = None) -> Dict[str, Any]:
        raw_resp = await self.client.get(url, params)
        raise_request_exception(raw_resp)
        resp = raw_resp.json()
        self._check_pageable(resp)
        return resp

    def stream(
        self,
    ) -> Union[
        AsyncGenerator[Dict[str, Any], None], Generator[Dict[str, Any], None, None]
    ]:
        """Creates an EventSource that listens for incoming messages from the server.

        See `Horizon Response Format <https://www.stellar.org/developers/horizon/reference/responses.html>`_

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`_

        :return: If it is called synchronous, it will return ``Generator``, If
            it is called asynchronously, it will return ``AsyncGenerator``.

        :raise: :exc:`StreamClientError <stellar_sdk.exceptions.StreamClientError>` - Failed to fetch stream resource.
        """
        if self.__async:
            return self.__stream_async()
        else:
            return self.__stream_sync()

    async def __stream_async(self) -> AsyncGenerator[Dict[str, Any], None]:
        url = urljoin_with_query(self.horizon_url, self.endpoint)
        stream = self.client.stream(url, self.params)
        while True:
            yield await stream.__anext__()

    def __stream_sync(self) -> Generator[Dict[str, Any], None, None]:
        url = urljoin_with_query(self.horizon_url, self.endpoint)
        return self.client.stream(url, self.params)

    def cursor(self, cursor: Union) -> "BaseCallBuilder":
        """Sets ``cursor`` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        See `Paging <https://www.stellar.org/developers/horizon/reference/paging.html>`_

        :param cursor: A cursor is a value that points to a specific location in a collection of resources.
        :return: current CallBuilder instance
        """
        self._add_query_param("cursor", cursor)
        return self

    def limit(self, limit: int) -> "BaseCallBuilder":
        """Sets ``limit`` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        See `Paging <https://www.stellar.org/developers/horizon/reference/paging.html>`_

        :param limit: Number of records the server should return.
        :return:
        """
        self._add_query_param("limit", limit)
        return self

    def order(self, desc: bool = True) -> "BaseCallBuilder":
        """Sets ``order`` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        :param desc: Sort direction, ``True`` to get desc sort direction, the default setting is ``True``.
        :return: current CallBuilder instance
        """
        order = "asc"
        if desc:
            order = "desc"
        self._add_query_param("order", order)
        return self

    def next(self):
        if self.next_href is None:
            raise NotPageableError("The next page does not exist.")
        return self.__call(self.next_href, None)

    def prev(self):
        if self.prev_href is None:
            raise NotPageableError("The prev page does not exist.")
        return self.__call(self.prev_href, None)

    def _add_query_param(self, key: str, value: Union[str, float, int, bool, None]):
        if value is None:
            pass  # pragma: no cover
        elif value is True:
            self.params[key] = "true"
        elif value is False:
            self.params[key] = "false"
        else:
            self.params[key] = str(value)

    def _check_pageable(self, response: dict) -> None:
        links = response.get("_links")
        if not links:
            return
        prev_page = links.get("prev")
        next_page = links.get("next")
        if prev_page:
            self.prev_href = prev_page.get("href")
        if next_page:
            self.next_href = next_page.get("href")

    def _add_query_params(
        self, params: Mapping[str, Union[str, float, int, bool, None]]
    ) -> None:
        for k, v in params.items():
            self._add_query_param(k, v)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.client == other.client
            and self.params == other.params
            and self.endpoint == other.endpoint
            and self.horizon_url == other.horizon_url
        )
