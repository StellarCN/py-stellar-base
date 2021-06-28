from abc import ABCMeta, abstractmethod
from typing import Dict, Any, Generator

from .response import Response

__all__ = ["BaseSyncClient"]


class BaseSyncClient(metaclass=ABCMeta):
    """This is an abstract class,
    and if you want to implement your own synchronous client, you **must** implement this class.

    """

    @abstractmethod
    def get(self, url: str, params: Dict[str, str] = None) -> Response:
        """Perform HTTP GET request.

        :param url: the request url
        :param params: the request params
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        pass

    @abstractmethod
    def post(self, url: str, data: Dict[str, str]) -> Response:
        """Perform HTTP POST request.

        :param url: the request url
        :param data: the data send to server
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        pass

    @abstractmethod
    def stream(
        self, url: str, params: Dict[str, str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Creates an EventSource that listens for incoming messages from the server.

        See `Horizon Response Format <https://www.stellar.org/developers/horizon/reference/responses.html>`_

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`_

        :param url: the request url
        :param params: the request params
        :return: a dict Generator for server response
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        pass

    @abstractmethod
    def close(self):
        pass
