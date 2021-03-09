import json
from typing import Generator, Union, Dict, Any, Tuple

import requests
from requests import Session, RequestException
from requests.adapters import HTTPAdapter, DEFAULT_POOLSIZE
from sseclient import SSEClient
from urllib3.exceptions import NewConnectionError
from urllib3.util import Retry

from . import defines
from ..__version__ import __version__
from ..client.base_sync_client import BaseSyncClient
from ..client.response import Response
from ..exceptions import ConnectionError

DEFAULT_NUM_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
USER_AGENT = f"py-stellar-sdk/{__version__}/RequestsClient"
IDENTIFICATION_HEADERS = {
    "X-Client-Name": "py-stellar-sdk",
    "X-Client-Version": __version__,
}

__all__ = ["RequestsClient"]


class RequestsClient(BaseSyncClient):
    """The :class:`RequestsClient` object is a synchronous http client,
    which represents the interface for making requests to a server instance.

    :param pool_size: persistent connection to Horizon and connection pool
    :param num_retries: configurable request retry functionality
    :param request_timeout: the timeout for all GET requests
    :param post_timeout: the timeout for all POST requests
    :param backoff_factor: a backoff factor to apply between attempts after the second try
    :param session: the request session
    :param stream_session: the stream request session
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
    ):
        self.pool_size: int = pool_size
        self.num_retries: int = num_retries
        self.request_timeout: int = request_timeout
        self.post_timeout: float = post_timeout
        self.backoff_factor: float = backoff_factor

        # adding 504 to the tuple of statuses to retry
        self.status_forcelist: Tuple[int] = tuple(Retry.RETRY_AFTER_STATUS_CODES) + (
            504,
        )

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

        headers = {**IDENTIFICATION_HEADERS, "User-Agent": USER_AGENT}

        # init session
        if session is None:
            session = requests.Session()

            # set default headers
            session.headers.update(headers)

            session.mount("http://", adapter)
            session.mount("https://", adapter)
        self._session: Session = session

        if stream_session is None:
            # configure SSE session (differs from our standard session)
            stream_session = requests.Session()

            sse_retry = Retry(
                total=1000000, redirect=0, status_forcelist=self.status_forcelist
            )
            sse_adapter = HTTPAdapter(
                pool_connections=self.pool_size,
                pool_maxsize=self.pool_size,
                max_retries=sse_retry,
            )

            stream_session.headers.update(headers)
            stream_session.mount("http://", sse_adapter)
            stream_session.mount("https://", sse_adapter)
        self._stream_session: Session = stream_session

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

    def post(self, url: str, data: Dict[str, str] = None) -> Response:
        """Perform HTTP POST request.

        :param url: the request url
        :param data: the data send to server
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        try:
            resp = self._session.post(url, data=data, timeout=self.post_timeout)
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

        See `Horizon Response Format <https://www.stellar.org/developers/horizon/reference/responses.html>`_

        See `MDN EventSource <https://developer.mozilla.org/en-US/docs/Web/API/EventSource>`_

        :param url: the request url
        :param params: the request params
        :return: a Generator for server response
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        query_params: Dict[str, Union[int, float, str]] = {**IDENTIFICATION_HEADERS}
        if params:
            query_params = {**params, **query_params}
        stream_client = _SSEClient(
            url,
            retry=0,
            session=self._stream_session,
            connect_retry=-1,
            params=query_params,
        )
        for message in stream_client:
            yield message

    def close(self) -> None:
        """Close underlying connector.

        Release all acquired resources.
        """
        self._session.close()
        self._stream_session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class _SSEClient:
    def __init__(
        self,
        url: str,
        last_id: Union[str, int] = None,
        retry: int = 3000,
        session: Session = None,
        chunk_size: int = 1024,
        connect_retry: int = 0,
        **kwargs,
    ):
        if SSEClient is None:
            raise ImportError(
                "SSE not supported, missing `stellar-base-sseclient` module"
            )  # pragma: no cover

        self.client = SSEClient(
            url, last_id, retry, session, chunk_size, connect_retry, **kwargs
        )

    def __iter__(self):
        return self

    def __next__(self) -> Dict[str, Any]:
        while True:
            msg = next(self.client)
            data = msg.data
            if data != '"hello"' and data != '"byebye"':
                return json.loads(data)
