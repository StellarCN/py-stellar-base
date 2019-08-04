import json
from typing import Generator

import requests
from requests import Session
from requests.adapters import HTTPAdapter, DEFAULT_POOLSIZE
from sseclient import SSEClient
from urllib3.util import Retry

from ..__version__ import __version__
from ..client.base_sync_client import BaseSyncClient
from ..client.response import Response

# two ledgers + 1 sec, let's retry faster and not wait 60 secs.
DEFAULT_REQUEST_TIMEOUT = 11
DEFAULT_NUM_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
USER_AGENT = "py-stellar-sdk/%s/RequestsClient" % __version__
IDENTIFICATION_HEADERS = {
    "X-Client-Name": "py-stellar-sdk",
    "X-Client-Version": __version__,
}


class RequestsClient(BaseSyncClient):
    def __init__(
        self,
        pool_size: int = DEFAULT_POOLSIZE,
        num_retries: int = DEFAULT_NUM_RETRIES,
        request_timeout: int = DEFAULT_REQUEST_TIMEOUT,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        session: Session = None,
        stream_session: Session = None,
    ):
        self.pool_size = pool_size
        self.num_retries = num_retries
        self.request_timeout = request_timeout
        self.backoff_factor = backoff_factor

        # adding 504 to the tuple of statuses to retry
        self.status_forcelist = tuple(Retry.RETRY_AFTER_STATUS_CODES) + (504,)

        # configure standard session

        # configure retry handler
        retry = Retry(
            total=self.num_retries,
            backoff_factor=self.backoff_factor,
            redirect=0,
            status_forcelist=self.status_forcelist,
            method_whitelist=frozenset(["GET", "POST"]),
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
        self._session = session
        if self._session is None:
            session = requests.Session()

            # set default headers
            session.headers.update(headers)

            session.mount("http://", adapter)
            session.mount("https://", adapter)
            self._session = session

        self._stream_session = stream_session
        if self._stream_session is None:
            # configure SSE session (differs from our standard session)
            sse_retry = Retry(
                total=1000000, redirect=0, status_forcelist=self.status_forcelist
            )
            sse_adapter = HTTPAdapter(
                pool_connections=self.pool_size,
                pool_maxsize=self.pool_size,
                max_retries=sse_retry,
            )
            sse_session = requests.Session()
            sse_session.headers.update(headers)
            sse_session.mount("http://", sse_adapter)
            sse_session.mount("https://", sse_adapter)
            self._stream_session = sse_session

    def get(self, url, params=None) -> Response:
        resp = self._session.get(url, params=params, timeout=self.request_timeout)
        return Response(
            status_code=resp.status_code,
            text=resp.text,
            headers=dict(resp.headers),
            url=resp.url,
        )

    def post(self, url, data=None) -> Response:
        resp = self._session.post(url, data=data, timeout=self.request_timeout)
        return Response(
            status_code=resp.status_code,
            text=resp.text,
            headers=dict(resp.headers),
            url=resp.url,
        )

    def stream(self, url, params=None) -> Generator[dict, None, None]:
        if params:
            params = {**params, **IDENTIFICATION_HEADERS}
        else:
            params = IDENTIFICATION_HEADERS  # pragma: no cover
        stream_client = _SSEClient(
            url, retry=0, session=self._stream_session, connect_retry=-1, params=params
        )
        for message in stream_client:
            yield message

    def close(self) -> None:
        self._session.close()
        self._stream_session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class _SSEClient:
    def __init__(
        self,
        url,
        last_id=None,
        retry=3000,
        session=None,
        chunk_size=1024,
        connect_retry=0,
        **kwargs
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

    def __next__(self):
        while True:
            msg = next(self.client)
            data = msg.data
            if data != '"hello"' and data != '"byebye"':
                return json.loads(data)
