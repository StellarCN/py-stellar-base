import asyncio
import json
from typing import Optional, Union, AsyncGenerator

import aiohttp
from aiohttp_sse_client.client import EventSource

from .base_async_client import BaseAsyncClient
from ..__version__ import __version__

DEFAULT_REQUEST_TIMEOUT = 11  # two ledgers + 1 sec, let's retry faster and not wait 60 secs.
DEFAULT_NUM_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
USER_AGENT = {
    'X-Client-Name': 'py-stellar-sdk',
    'X-Client-Version': __version__,
}


class AiohttpClient(BaseAsyncClient):

    def __init__(self,
                 pool_size: Optional[int] = None,
                 num_retries: Optional[int] = DEFAULT_NUM_RETRIES,
                 request_timeout: Optional[Union[int, None]] = DEFAULT_REQUEST_TIMEOUT,
                 backoff_factor: Optional[float] = DEFAULT_BACKOFF_FACTOR,
                 user_agent: Optional[dict] = None,
                 **kwargs) -> None:
        self.num_retries = num_retries
        self.backoff_factor = backoff_factor

        # init session
        if pool_size is None:
            connector = aiohttp.TCPConnector()
        else:
            connector = aiohttp.TCPConnector(limit=pool_size)

        self.user_agent = USER_AGENT
        if user_agent:
            self.user_agent = user_agent

        headers = {
            **self.user_agent,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        session = aiohttp.ClientSession(headers=headers,
                                        connector=connector,
                                        timeout=aiohttp.ClientTimeout(total=request_timeout),
                                        **kwargs)

        self._session = session
        self._sse_session = None

    async def get(self, url: str, params=None) -> dict:
        async with self._session.get(url, params=params) as response:
            return await response.json(encoding='utf-8')

    async def post(self, url: str, params=None) -> dict:
        async with self._session.post(url, params=params) as response:
            return await response.json(encoding='utf-8')

    async def _init_sse_session(self) -> None:
        """Init the sse session """
        if self._sse_session is None:
            self._sse_session = aiohttp.ClientSession()  # No timeout, no special connector
            # Other headers such as "Accept: text/event-stream" are added by thr SSEClient

    async def stream(self, url: str, params: Optional[dict] = None) -> AsyncGenerator[dict]:
        """
        SSE generator with timeout between events
        :param url: URL to send SSE request to
        :param params: params
        :return: response dict
        """

        async def _sse_generator() -> AsyncGenerator[dict]:
            """
            Generator for sse events
            """
            if params.get('cursor') is None:
                params['cursor'] = 'now'  # Start monitoring from now.
            params.update(**self.user_agent)
            retry = 0.1
            while True:
                try:
                    """
                    Create a new SSEClient:
                    Using the last id as the cursor
                    Headers are needed because of a bug that makes "params" override the default headers
                    """
                    async with EventSource(url, session=self._sse_session,
                                           params=params) as client:
                        """
                        We want to throw a TimeoutError if we didnt get any event in the last x seconds.
                        read_timeout in aiohttp is not implemented correctly https://github.com/aio-libs/aiohttp/issues/1954
                        So we will create our own way to do that.

                        Note that the timeout starts from the first event forward. There is no until we get the first event.
                        """
                        async for event in client:
                            if event.last_event_id != '':
                                # Events that dont have an id are not useful for us (hello/byebye events)
                                # Save the last event id and retry time
                                last_id = event.last_event_id
                                retry = client._reconnection_time.total_seconds()
                                try:
                                    data = event.data
                                    if data != '"hello"' and data != '"byebye"':
                                        yield json.loads(data)
                                except json.JSONDecodeError:
                                    # Content was not json-decodable
                                    pass
                except aiohttp.ClientPayloadError:
                    # Retry if the connection dropped after we got the initial response
                    await asyncio.sleep(retry)

        await self._init_sse_session()
        gen = _sse_generator()
        while True:
            yield await gen.__anext__()

    async def __aenter__(self) -> 'AiohttpClient':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self._session.__aexit__(None, None, None)
        if self._sse_session is not None:
            await self._sse_session.__aexit__(None, None, None)
