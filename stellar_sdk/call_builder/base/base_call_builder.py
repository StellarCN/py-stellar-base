from typing import (
    Any,
    AsyncGenerator,
    Coroutine,
    Dict,
    Generator,
    Mapping,
    Optional,
    Union,
)

__all__ = ["BaseCallBuilder"]


class BaseCallBuilder:
    """Creates a new :class:`BaseCallBuilder` pointed to server defined by horizon_url.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
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
        raise NotImplementedError

    def stream(
        self,
    ) -> Union[
        AsyncGenerator[Dict[str, Any], None], Generator[Dict[str, Any], None, None]
    ]:
        """Creates an EventSource that listens for incoming messages from the server.

        See `Horizon Response Format <https://developers.stellar.org/api/introduction/response-format/>`__

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`__

        :return: If it is called synchronous, it will return ``Generator``, If
            it is called asynchronously, it will return ``AsyncGenerator``.

        :raise: :exc:`StreamClientError <stellar_sdk.exceptions.StreamClientError>` - Failed to fetch stream resource.
        """
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def prev(self):
        raise NotImplementedError

    def cursor(self, cursor: Union[int, str]):
        """Sets ``cursor`` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        See `Pagination <https://developers.stellar.org/api/introduction/pagination/>`__

        :param cursor: A cursor is a value that points to a specific location in a collection of resources.
        :return: current CallBuilder instance
        """
        self._add_query_param("cursor", cursor)
        return self

    def limit(self, limit: int):
        """Sets ``limit`` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        See `Pagination <https://developers.stellar.org/api/introduction/pagination/>`__

        :param limit: Number of records the server should return.
        :return:
        """
        self._add_query_param("limit", limit)
        return self

    def order(self, desc: bool = True):
        """Sets `order` parameter for the current call. Returns the CallBuilder object on which this method has been called.

        :param desc: Sort direction, ``True`` to get desc sort direction, the default setting is ``True``.
        :return: current CallBuilder instance
        """
        order = "asc"
        if desc:
            order = "desc"
        self._add_query_param("order", order)
        return self

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
