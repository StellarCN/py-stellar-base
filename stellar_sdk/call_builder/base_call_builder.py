from typing import (
    Union,
    Coroutine,
    Any,
    Dict,
    Mapping,
    Generator,
    AsyncGenerator,
    Optional,
    TypeVar,
    Generic,
    Type,
    Callable,
)

from pydantic import BaseModel

from ..__version__ import __issues__
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..exceptions import raise_request_exception, NotPageableError
from ..response.wrapped_response import WrappedResponse
from ..utils import urljoin_with_query

T = TypeVar("T")
S = TypeVar("S", bound="BaseCallBuilder")


class BaseCallBuilder(Generic[T]):
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

    def call(
        self,
    ) -> Union[WrappedResponse[T], Coroutine[Any, Any, WrappedResponse[T]]]:
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
        return self._call(url, self.params)

    def _call(
        self, url: str, params: dict = None
    ) -> Union[WrappedResponse[T], Coroutine[Any, Any, WrappedResponse[T]]]:
        if self.__async:
            return self._call_async(url, params)
        else:
            return self._call_sync(url, params)

    def _call_sync(self, url: str, params: dict = None) -> WrappedResponse[T]:
        raw_resp = self.client.get(url, params)
        raise_request_exception(raw_resp)
        resp = raw_resp.json()
        self._set_page_link(resp)
        return WrappedResponse(
            parse_func=self._parse_response, raw_response=raw_resp, builder=self
        )

    async def _call_async(self, url: str, params: dict = None) -> WrappedResponse[T]:
        raw_resp = await self.client.get(url, params)
        raise_request_exception(raw_resp)
        resp = raw_resp.json()
        self._set_page_link(resp)
        return WrappedResponse(
            parse_func=self._parse_response, raw_response=raw_resp, builder=self
        )

    def _parse_response(self, raw_data):
        raise NotImplementedError(
            "This endpoint has not implemented this feature, "
            "please submit an issue: %s" % __issues__
        )

    def _base_parse_response(
        self,
        raw_data,
        model: Type[BaseModel] = None,
        model_selector: Callable[[dict], Type[BaseModel]] = None,
    ):
        if self._check_pageable(raw_data):
            if model_selector is not None:
                parsed = [
                    model_selector(record).parse_obj(record)
                    for record in raw_data["_embedded"]["records"]
                ]
            else:
                parsed = [
                    model.parse_obj(record)
                    for record in raw_data["_embedded"]["records"]
                ]
        else:
            if model_selector is not None:
                parsed = model_selector(raw_data).parse_obj(raw_data)
            else:
                parsed = model.parse_obj(raw_data)
        return parsed

    def _stream(
        self,
    ) -> Union[
        AsyncGenerator[WrappedResponse, None], Generator[WrappedResponse, None, None]
    ]:
        """Creates an EventSource that listens for incoming messages from the server.

        See `Horizon Response Format <https://www.stellar.org/developers/horizon/reference/responses.html>`_

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`_

        :return: If it is called synchronous, it will return ``Generator``, If
            it is called asynchronously, it will return ``AsyncGenerator``.
        """
        if self.__async:
            return self._stream_async()
        else:
            return self._stream_sync()

    async def _stream_async(self) -> AsyncGenerator[WrappedResponse, None]:
        url = urljoin_with_query(self.horizon_url, self.endpoint)
        stream = self.client.stream(url, self.params)
        while True:
            yield WrappedResponse(
                parse_func=self._parse_response,
                raw_data=(await stream.__anext__()),
                builder=self,
            )

    def _stream_sync(self) -> Generator[WrappedResponse, None, None]:
        url = urljoin_with_query(self.horizon_url, self.endpoint)
        stream = self.client.stream(url, self.params)
        while True:
            yield WrappedResponse(
                parse_func=self._parse_response,
                raw_data=stream.__next__(),
                builder=self,
            )

    def cursor(self: S, cursor: Union[str, int]) -> S:
        """Sets ``cursor`` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        See `Paging <https://www.stellar.org/developers/horizon/reference/paging.html>`_

        :param cursor: A cursor is a value that points to a specific location in a collection of resources.
        :return: current CallBuilder instance
        """
        self._add_query_param("cursor", cursor)
        return self

    def limit(self: S, limit: int) -> S:
        """Sets ``limit`` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        See `Paging <https://www.stellar.org/developers/horizon/reference/paging.html>`_

        :param limit: Number of records the server should return.
        :return:
        """
        self._add_query_param("limit", limit)
        return self

    def order(self: S, desc: bool = True) -> S:
        """Sets ``order`` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        :param desc: Sort direction, ``True`` to get desc sort direction, the default setting is ``True``.
        :return: current CallBuilder instance
        """
        order = "asc"
        if desc:
            order = "desc"
        self._add_query_param("order", order)
        return self

    def next(
        self,
    ) -> Union[WrappedResponse[T], Coroutine[Any, Any, WrappedResponse[T]]]:
        if self.next_href is None:
            raise NotPageableError("The next page does not exist.")
        return self._call(self.next_href, None)

    def prev(
        self,
    ) -> Union[WrappedResponse[T], Coroutine[Any, Any, WrappedResponse[T]]]:
        if self.prev_href is None:
            raise NotPageableError("The prev page does not exist.")
        return self._call(self.prev_href, None)

    def _add_query_param(
        self, key: str, value: Union[str, float, int, bool, None]
    ) -> None:
        if value is None:
            pass
        elif value is True:
            self.params[key] = "true"
        elif value is False:
            self.params[key] = "false"
        else:
            self.params[key] = str(value)

    def _set_page_link(self, response: dict) -> None:
        links = response.get("_links")
        if not links:
            return
        prev_page = links.get("prev")
        next_page = links.get("next")
        if prev_page:
            self.prev_href = prev_page.get("href")
        if next_page:
            self.next_href = next_page.get("href")

    def _check_pageable(self, raw_data: dict) -> bool:
        if "_embedded" in raw_data.keys() and "records" in raw_data["_embedded"].keys():
            return True
        return False

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
