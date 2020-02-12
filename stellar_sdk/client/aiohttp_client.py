import asyncio
import json
import logging
from typing import Optional, AsyncGenerator, Any, Dict

import aiohttp
from aiohttp_sse_client.client import EventSource

from .base_async_client import BaseAsyncClient
from .response import Response
from ..__version__ import __version__

logger = logging.getLogger(__name__)

# four ledgers sec, let's retry faster and not wait 60 secs.
DEFAULT_REQUEST_TIMEOUT = 20
DEFAULT_NUM_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
USER_AGENT = "py-stellar-sdk/%s/AiohttpClient" % __version__
IDENTIFICATION_HEADERS = {
    "X-Client-Name": "py-stellar-sdk",
    "X-Client-Version": __version__,
}

__all__ = ["AiohttpClient"]


class AiohttpClient(BaseAsyncClient):
    """The :class:`AiohttpClient` object is a asynchronous http client,
    which represents the interface for making requests to a server instance.

    :param pool_size: persistent connection to Horizon and connection pool
    :param request_timeout: the timeout for all requests
    :param backoff_factor: a backoff factor to apply between attempts after the second try
    :param user_agent: the server can use it to identify you
    """

    def __init__(
        self,
        pool_size: Optional[int] = None,
        request_timeout: float = DEFAULT_REQUEST_TIMEOUT,
        backoff_factor: Optional[float] = DEFAULT_BACKOFF_FACTOR,
        user_agent: Optional[str] = None,
        **kwargs
    ) -> None:
        self.backoff_factor: Optional[float] = backoff_factor
        self.request_timeout: float = request_timeout

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
            **kwargs
        )

        self._session: aiohttp.ClientSession = session
        self._sse_session: Optional[aiohttp.ClientSession] = None

    async def get(self, url: str, params: Dict[str, str] = None) -> Response:
        """Perform HTTP GET request.

        :param url: the request url
        :param params: the requested params
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
            response = await self._session.post(url, data=data)
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
        """Init the sse session """
        if self._sse_session is None:
            # No timeout, no special connector
            # Other headers such as "Accept: text/event-stream" are added by thr SSEClient
            self._sse_session = aiohttp.ClientSession()

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
                            pass
            except aiohttp.ClientConnectionError:
                # Retry if the connection dropped after we got the initial response
                logger.warning(
                    "We have encountered an error and we will try to reconnect, cursor = {}".format(
                        query_params.get("cursor")
                    )
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
