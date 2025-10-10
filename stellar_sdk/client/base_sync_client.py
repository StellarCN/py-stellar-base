from abc import ABCMeta, abstractmethod
from collections.abc import Generator
from typing import Any

from .response import Response

__all__ = ["BaseSyncClient"]


class BaseSyncClient(metaclass=ABCMeta):
    """This is an abstract class,
    and if you want to implement your own synchronous client, you **must** implement this class.

    """

    @abstractmethod
    def get(self, url: str, params: dict[str, str] | None = None) -> Response:
        """Perform HTTP GET request.

        :param url: the request url
        :param params: the request params
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """

    @abstractmethod
    def post(
        self,
        url: str,
        data: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> Response:
        """Perform HTTP POST request.

        :param url: the request url
        :param data: the data send to server
        :param json_data: the json data send to server
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """

    @abstractmethod
    def stream(
        self, url: str, params: dict[str, str] | None = None
    ) -> Generator[dict[str, Any], None, None]:
        """Creates an EventSource that listens for incoming messages from the server.

        See `Horizon Response Format <https://developers.stellar.org/docs/data/apis/horizon/api-reference/structure/response-format>`__

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`_

        :param url: the request url
        :param params: the request params
        :return: a dict Generator for server response
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """

    @abstractmethod
    def close(self):
        pass
