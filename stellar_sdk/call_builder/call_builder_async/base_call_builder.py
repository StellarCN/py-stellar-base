from typing import Any, AsyncGenerator, Dict

from ...call_builder.base.base_call_builder import BaseCallBuilder as _BaseCallBuilder
from ...client.base_async_client import BaseAsyncClient
from ...client.response import Response
from ...exceptions import NotPageableError, raise_request_exception
from ...utils import urljoin_with_query

__all__ = ["BaseCallBuilder"]


class BaseCallBuilder(_BaseCallBuilder):
    """Creates a new :class:`BaseCallBuilder` pointed to server defined by horizon_url.

    This is an **abstract** class. Do not create this object directly, use :class:`stellar_sdk.ServerAsync` class.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(self, client: BaseAsyncClient, **kwargs) -> None:
        super().__init__(**kwargs)
        self.client: BaseAsyncClient = client

    async def call(self) -> Dict[str, Any]:
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
        return await self._call(url, self.params)

    async def _call(self, url: str, params: dict = None) -> Dict[str, Any]:
        raw_resp = await self.client.get(url, params)
        assert isinstance(raw_resp, Response)
        raise_request_exception(raw_resp)
        resp = raw_resp.json()
        self._check_pageable(resp)
        return resp

    async def stream(
        self,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Creates an EventSource that listens for incoming messages from the server.

        See `Horizon Response Format <https://developers.stellar.org/api/introduction/response-format/>`__

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`__

        :return: an EventSource.

        :raise: :exc:`StreamClientError <stellar_sdk.exceptions.StreamClientError>` - Failed to fetch stream resource.
        """
        url = urljoin_with_query(self.horizon_url, self.endpoint)
        stream: AsyncGenerator[Dict[str, Any], None] = self.client.stream(url, self.params)  # type: ignore[assignment]
        while True:
            yield await stream.__anext__()

    async def next(self) -> Dict[str, Any]:
        if self.next_href is None:
            raise NotPageableError("The next page does not exist.")
        return await self._call(self.next_href, None)

    async def prev(self) -> Dict[str, Any]:
        if self.prev_href is None:
            raise NotPageableError("The prev page does not exist.")
        return await self._call(self.prev_href, None)

    def __hash__(self):
        return hash(
            (
                self.params,
                self.endpoint,
                self.horizon_url,
                self.client,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.params == other.params
            and self.endpoint == other.endpoint
            and self.horizon_url == other.horizon_url
            and self.client == other.client
        )

    def __repr__(self):
        return (
            f"<CallBuilder [horizon_url={self.horizon_url}, "
            f"endpoint={self.endpoint}, "
            f"params={self.params}, "
            f"prev_href={self.prev_href}, "
            f"next_href={self.next_href}, "
            f"client={self.client}]>"
        )
