import json
import logging
import time
from typing import Any, Dict, Generator, Optional, Tuple

import requests
from requests import RequestException, Session
from requests.adapters import DEFAULT_POOLSIZE, HTTPAdapter
from requests_sse import EventSource
from urllib3.exceptions import NewConnectionError
from urllib3.util import Retry

from ..__version__ import __version__
from ..client.base_sync_client import BaseSyncClient
from ..client.response import Response
from ..exceptions import ConnectionError, StreamClientError
from . import defines

DEFAULT_NUM_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
USER_AGENT = f"py-stellar-base/{__version__}/RequestsClient"
IDENTIFICATION_HEADERS = {
    "X-Client-Name": "py-stellar-base",
    "X-Client-Version": __version__,
}

logger = logging.getLogger(__name__)

__all__ = ["RequestsClient"]


class RequestsClient(BaseSyncClient):
    """The :class:`RequestsClient` object is a synchronous http client,
    which represents the interface for making requests to a server instance.

    :param pool_size: persistent connection to Horizon and connection pool
    :param num_retries: configurable request retry functionality
    :param request_timeout: the timeout for all GET requests (for each retry)
    :param post_timeout: the timeout for all POST requests (for each retry)
    :param backoff_factor: a backoff factor to apply between attempts after the second try
    :param session: the request session
    :param stream_session: the stream request session
    :param custom_headers: any additional HTTP headers to add in requests
    """

    def __init__(
        self,
        pool_size: int = DEFAULT_POOLSIZE,
        num_retries: int = DEFAULT_NUM_RETRIES,
        request_timeout: int = defines.DEFAULT_GET_TIMEOUT_SECONDS,
        post_timeout: float = defines.DEFAULT_POST_TIMEOUT_SECONDS,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        session: Session = None,
        stream_session: Session = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ):
        self.pool_size: int = pool_size
        self.num_retries: int = num_retries
        self.request_timeout: int = request_timeout
        self.post_timeout: float = post_timeout
        self.backoff_factor: float = backoff_factor

        # adding 504 to the tuple of statuses to retry
        self.status_forcelist: Tuple[int] = tuple(Retry.RETRY_AFTER_STATUS_CODES) + (
            504,
        )  # type: ignore[assignment]

        # configure standard session

        # configure retry handler
        retry = Retry(
            total=self.num_retries,
            backoff_factor=self.backoff_factor,
            redirect=0,
            status_forcelist=self.status_forcelist,
            allowed_methods=frozenset(["GET", "POST"]),
            raise_on_status=False,
        )
        # init transport adapter
        adapter = HTTPAdapter(
            pool_connections=self.pool_size,
            pool_maxsize=self.pool_size,
            max_retries=retry,
        )

        self.headers = {**IDENTIFICATION_HEADERS, "User-Agent": USER_AGENT}

        if custom_headers:
            self.headers = {**self.headers, **custom_headers}

        # init session
        if session is None:
            session = requests.Session()

            # set default headers
            session.headers.update(self.headers)

            session.mount("http://", adapter)
            session.mount("https://", adapter)
        self._session: Session = session
        self._stream_session: Optional[Session] = stream_session

    def get(self, url: str, params: Dict[str, str] = None) -> Response:
        """Perform HTTP GET request.

        :param url: the request url
        :param params: the request params
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        try:
            resp = self._session.get(url, params=params, timeout=self.request_timeout)
        except (RequestException, NewConnectionError) as err:
            raise ConnectionError(err)
        return Response(
            status_code=resp.status_code,
            text=resp.text,
            headers=dict(resp.headers),
            url=resp.url,
        )

    def post(
        self, url: str, data: Dict[str, str] = None, json_data: Dict[str, Any] = None
    ) -> Response:
        """Perform HTTP POST request.

        :param url: the request url
        :param data: the data send to server
        :param json_data: the json data send to server
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        try:
            resp = self._session.post(
                url, data=data, json=json_data, timeout=self.post_timeout
            )
        except (RequestException, NewConnectionError) as err:
            raise ConnectionError(err)
        return Response(
            status_code=resp.status_code,
            text=resp.text,
            headers=dict(resp.headers),
            url=resp.url,
        )

    def stream(
        self, url: str, params: Dict[str, str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Creates an EventSource that listens for incoming messages from the server.

        See `Horizon Response Format <https://developers.stellar.org/api/introduction/response-format/>`__

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`_

        :param url: the request url
        :param params: the request params
        :return: a Generator for server response
        :raise: :exc:`StreamClientError <stellar_sdk.exceptions.StreamClientError>`
        """
        query_params = {**params} if params else dict()

        query_params.update(**IDENTIFICATION_HEADERS)
        retry = 0.1

        while True:
            try:
                """
                Create a new SSEClient:
                Using the last id as the cursor
                """
                with EventSource(
                    url,
                    timeout=60,
                    params=query_params,
                    headers=self.headers,
                ) as client:
                    for event in client:
                        if event.last_event_id:
                            query_params["cursor"] = event.last_event_id
                            # Events that dont have an id are not useful for us (hello/byebye events)
                        retry = client._reconnection_time.total_seconds()
                        try:
                            data = event.data
                            if data != '"hello"' and data != '"byebye"':
                                yield json.loads(data)
                        except json.JSONDecodeError:
                            # Content was not json-decodable
                            pass  # pragma: no cover
            except requests.Timeout:
                logger.warning(
                    f"We have encountered an timeout error and we will try to reconnect, cursor = {query_params.get('cursor')}"
                )
                time.sleep(retry)
            except requests.RequestException as e:
                raise StreamClientError(
                    query_params["cursor"], "Failed to get stream message."
                ) from e

    def close(self) -> None:
        """Close underlying connector.

        Release all acquired resources.
        """
        self._session.close()
        if self._stream_session:
            self._stream_session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return (
            f"<RequestsClient [pool_size={self.pool_size}, "
            f"num_retries={self.num_retries}, "
            f"request_timeout={self.request_timeout}, "
            f"post_timeout={self.post_timeout}, "
            f"backoff_factor={self.backoff_factor}, "
            f"session={self._session}, "
            f"stream_session={self.backoff_factor}]>"
        )
