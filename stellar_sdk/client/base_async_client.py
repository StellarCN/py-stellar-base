from abc import ABCMeta, abstractmethod
from typing import Any, AsyncGenerator, Dict

from .response import Response

__all__ = ["BaseAsyncClient"]


class BaseAsyncClient(metaclass=ABCMeta):
    """This is an abstract class,
    and if you want to implement your own asynchronous client, you **must** implement this class.

    """

    @abstractmethod
    async def get(self, url: str, params: Dict[str, str] = None) -> Response:
        """Perform HTTP GET request.

        :param url: the request url
        :param params: the request params
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        pass  # pragma: no cover

    @abstractmethod
    async def post(
        self,
        url: str,
        data: Dict[str, str] = None,
        json_data: Dict[str, Any] = None,
    ) -> Response:
        """Perform HTTP POST request.

        :param url: the request url
        :param data: the data send to server
        :param json_data: the json data send to server
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        pass  # pragma: no cover

    @abstractmethod
    def stream(
        self, url: str, params: Dict[str, str] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Creates an EventSource that listens for incoming messages from the server.

        See `Horizon Response Format <https://developers.stellar.org/api/introduction/response-format/>`__

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`_

        :param url: the request url
        :param params: the request params
        :return: a dict AsyncGenerator for server response
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        pass  # pragma: no cover

    @abstractmethod
    async def close(self) -> None:
        pass  # pragma: no cover
