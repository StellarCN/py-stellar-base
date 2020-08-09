import asyncio
import json
import logging
from typing import Optional, AsyncGenerator, Any, Dict
import aiohttp

from aiohttp_sse_client.client import EventSource
from . import defines
from .base_async_client import BaseAsyncClient
from .response import Response
from ..__version__ import __version__
from ..exceptions import StreamClientError

logger = logging.getLogger(__name__)

DEFAULT_NUM_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
USER_AGENT = f"py-stellar-sdk/{__version__}/AiohttpClient"
IDENTIFICATION_HEADERS = {
    "X-Client-Name": "py-stellar-sdk",
    "X-Client-Version": __version__,
}

__all__ = ["AiohttpClient"]


# Temporary solution to solve the problem that
# `aiohttp_sse_client` cannot read long stream messages.
# Let's rewrite a stream lib later.
async def __readline(self) -> bytes:
    if self._exception is not None:
        raise self._exception

    line = []
    line_size = 0
    not_enough = True

    while not_enough:
        while self._buffer and not_enough:
            offset = self._buffer_offset
            ichar = self._buffer[0].find(b"\n", offset) + 1
            # Read from current offset to found b'\n' or to the end.
            data = self._read_nowait_chunk(ichar - offset if ichar else -1)
            line.append(data)
            line_size += len(data)
            if ichar:
                not_enough = False
            #
            # if line_size > self._high_water:
            #     raise ValueError('Line is too long')
        if self._eof:
            break

        if not_enough:
            await self._wait("readline")

    return b"".join(line)


aiohttp.streams.StreamReader.readline = __readline


class AiohttpClient(BaseAsyncClient):
    """The :class:`AiohttpClient` object is a asynchronous http client,
    which represents the interface for making requests to a server instance.

    :param pool_size: persistent connection to Horizon and connection pool
    :param request_timeout: the timeout for all GET requests
    :param post_timeout: the timeout for all POST requests
    :param backoff_factor: a backoff factor to apply between attempts after the second try
    :param user_agent: the server can use it to identify you
    """

    def __init__(
        self,
        pool_size: Optional[int] = None,
        request_timeout: float = defines.DEFAULT_GET_TIMEOUT_SECONDS,
        post_timeout: float = defines.DEFAULT_POST_TIMEOUT_SECONDS,
        backoff_factor: Optional[float] = DEFAULT_BACKOFF_FACTOR,
        user_agent: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.backoff_factor: Optional[float] = backoff_factor
        self.request_timeout: float = request_timeout
        self.post_timeout: float = post_timeout

        # init session
        if pool_size is None:
            connector = aiohttp.TCPConnector()
        else:
            connector = aiohttp.TCPConnector(limit=pool_size)

        self.user_agent: dict = USER_AGENT
        if user_agent:
            self.user_agent = user_agent

        self.headers: dict = {
            **IDENTIFICATION_HEADERS,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": self.user_agent,
        }
        session = aiohttp.ClientSession(
            headers=self.headers.copy(),
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=request_timeout),
            **kwargs,
        )

        self._session: aiohttp.ClientSession = session
        self._sse_session: Optional[aiohttp.ClientSession] = None

    async def get(self, url: str, params: Dict[str, str] = None) -> Response:
        """Perform HTTP GET request.

        :param url: the request url
        :param params: the request params
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        try:
            response = await self._session.get(url, params=params)
            return Response(
                status_code=response.status,
                text=await response.text(),
                headers=dict(response.headers),
                url=str(response.url),
            )
        except aiohttp.ClientError as e:  # TODO: need more research
            raise ConnectionError(e)

    async def post(self, url: str, data: Dict[str, str] = None) -> Response:
        """Perform HTTP POST request.

        :param url: the request url
        :param data: the data send to server
        :return: the response from server
        :raise: :exc:`ConnectionError <stellar_sdk.exceptions.ConnectionError>`
        """
        try:
            response = await self._session.post(
                url, data=data, timeout=aiohttp.ClientTimeout(total=self.post_timeout)
            )
            return Response(
                status_code=response.status,
                text=await response.text(),
                headers=dict(response.headers),
                url=str(response.url),
            )
        except aiohttp.ClientConnectionError as e:
            raise ConnectionError(e)

    async def stream(
        self, url: str, params: Dict[str, str] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Perform Stream request.

        :param url: the request url
        :param params: the request params
        :return: the stream response from server
        :raise: :exc:`StreamClientError <stellar_sdk.exceptions.StreamClientError>` - Failed to fetch stream resource.
        """

        # Init the sse session
        if self._sse_session is None:
            # No special connector
            # Other headers such as "Accept: text/event-stream" are added by thr SSEClient
            timeout = aiohttp.ClientTimeout(total=60 * 5)
            self._sse_session = aiohttp.ClientSession(timeout=timeout)

        query_params = {**params} if params else dict()

        if query_params.get("cursor") is None:
            query_params["cursor"] = "now"  # Start monitoring from now.

        query_params.update(**IDENTIFICATION_HEADERS)
        retry = 0.1

        while True:
            try:
                """
                Create a new SSEClient:
                Using the last id as the cursor
                Headers are needed because of a bug that makes "params" override the default headers
                """
                async with EventSource(
                    url,
                    session=self._sse_session,
                    params=query_params,
                    headers=self.headers.copy(),
                ) as client:
                    """
                    We want to throw a TimeoutError if we didnt get any event in the last x seconds.
                    read_timeout in aiohttp is not implemented correctly https://github.com/aio-libs/aiohttp/issues/1954
                    So we will create our own way to do that.

                    Note that the timeout starts from the first event forward. There is no until we get the first event.
                    """
                    async for event in client:
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
            except aiohttp.ClientError as e:
                raise StreamClientError(
                    query_params["cursor"], "Failed to get stream message."
                ) from e
            except asyncio.exceptions.TimeoutError:
                logger.warning(
                    f"We have encountered an timeout error and we will try to reconnect, cursor = {query_params.get('cursor')}"
                )
                await asyncio.sleep(retry)

    async def __aenter__(self) -> "AiohttpClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        """Close underlying connector.

        Release all acquired resources.
        """
        await self._session.__aexit__(None, None, None)
        if self._sse_session is not None:
            await self._sse_session.__aexit__(None, None, None)
